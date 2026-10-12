import json, os, re, time, html, hashlib, urllib.request, datetime as dt, email.utils
import xml.etree.ElementTree as ET

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36",
      "Accept": "*/*", "Accept-Language": "pt-BR,pt;q=0.9"}
def baixar(url, timeout=20, tent=2):
    err = None
    for i in range(tent):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read()
        except Exception as e:
            err = e; time.sleep(1 + i * 2)
    raise err
NS = {"content": "http://purl.org/rss/1.0/modules/content/", "media": "http://search.yahoo.com/mrss/",
      "atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
def limpa(t, n=220):
    t = html.unescape(re.sub(r"<[^>]+>", " ", t or "")); t = re.sub(r"\s+", " ", t).strip()
    return (t[:n-1] + "…") if len(t) > n else t
def img_de(*htmls):
    for h in htmls:
        m = re.search(r'<img[^>]+src="([^"]+)"', h or "")
        if m: return html.unescape(m.group(1))
    return ""
def ts_rss(s):
    try: return int(email.utils.parsedate_to_datetime(s).timestamp() * 1000)
    except Exception:
        try: return int(dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp() * 1000)
        except Exception: return int(time.time() * 1000)
TICK = re.compile(r"\b([A-Z]{4}(?:3|4|11))\b")
def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

pasta = "."
for raiz, dirs, arqs in os.walk("."):
    if ".git" in raiz: continue
    if "index.html" in arqs and "pablo-financas" in open(os.path.join(raiz, "index.html"), encoding="utf-8", errors="ignore").read():
        pasta = raiz; break
saida = os.path.join(pasta, "conteudo.json")
antigo = {}
if os.path.exists(saida):
    try: antigo = json.load(open(saida, encoding="utf-8"))
    except Exception: antigo = {}
fontes_old = {f["id"]: f for f in antigo.get("fontes", [])}
itens_old = {}
for it in antigo.get("itens", []): itens_old.setdefault(it["fonte"], []).append(it)
img_cache = {it["link"]: it.get("img", "") for it in antigo.get("itens", []) if it.get("img")}

fontes, itens = [], []
lista = os.path.join(pasta, "fontes.txt")
linhas = open(lista, encoding="utf-8").read().splitlines() if os.path.exists(lista) else []
for l in linhas:
    l = l.split("#")[0].strip() if not l.strip().startswith("#") else ""
    if not l: continue
    partes = [p.strip() for p in l.split("|")]
    if len(partes) < 3: continue
    tipo, nome, end = partes[0].lower(), partes[1], partes[2]
    desc = partes[3] if len(partes) > 3 else ""
    fid = ("n-" if tipo.startswith("not") else "c-") + slug(nome)
    f = {"id": fid, "tipo": "noticia" if tipo.startswith("not") else "canal", "nome": nome, "desc": desc, "end": end,
         "avatar": (fontes_old.get(fid) or {}).get("avatar", ""), "site": "", "ok": False, "erro": ""}
    novos = []
    try:
        if f["tipo"] == "noticia":
            raiz = ET.fromstring(baixar(end))
            ch = raiz.find("channel")
            f["site"] = (ch.findtext("link") or "").strip() if ch is not None else ""
            if not f["avatar"] and f["site"]:
                dom = re.sub(r"^https?://", "", f["site"]).split("/")[0]
                f["avatar"] = f"https://www.google.com/s2/favicons?domain={dom}&sz=128"
            for it in (ch.findall("item") if ch is not None else [])[:14]:
                titulo = limpa(it.findtext("title"), 200); link = (it.findtext("link") or "").strip()
                desc_h = it.findtext("description") or ""; cont = it.findtext("content:encoded", namespaces=NS) or ""
                img = ""
                mc = it.find("media:content", NS)
                if mc is None: mc = it.find("media:thumbnail", NS)
                if mc is not None: img = mc.get("url", "")
                enc = it.find("enclosure")
                if not img and enc is not None and "image" in (enc.get("type") or ""): img = enc.get("url", "")
                img = img or img_de(cont, desc_h) or img_cache.get(link, "")
                texto = titulo + " " + limpa(desc_h, 600) + " " + limpa(cont, 1500)
                tks = sorted(set(TICK.findall(texto)))[:6]
                novos.append({"id": "n" + hashlib.md5((fid + link).encode()).hexdigest()[:10], "fonte": fid, "tipo": "noticia", "titulo": titulo,
                              "link": link, "img": img, "ts": ts_rss(it.findtext("pubDate") or ""), "resumo": limpa(desc_h or cont, 220), "tickers": tks})
            # imagem da página (og:image) para as mais novas sem foto
            for n in [x for x in novos if not x["img"]][:4]:
                try:
                    h = baixar(n["link"], timeout=12, tent=1).decode("utf-8", "ignore")
                    m = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', h) or re.search(r'<meta[^>]+content="([^"]+)"[^>]+property="og:image"', h)
                    if m: n["img"] = html.unescape(m.group(1))
                except Exception: pass
        else:
            cid = end if end.startswith("UC") else (fontes_old.get(fid) or {}).get("cid", "")
            if not cid or not f["avatar"]:
                url = f"https://www.youtube.com/{end}" if end.startswith("@") else f"https://www.youtube.com/channel/{end}"
                h = baixar(url).decode("utf-8", "ignore")
                if not cid:
                    m = re.search(r'"(?:externalId|channelId)":"(UC[\w-]{20,})"', h) or re.search(r'channel/(UC[\w-]{20,})', h)
                    cid = m.group(1) if m else ""
                m = re.search(r'<meta property="og:image" content="([^"]+)"', h)
                if m: f["avatar"] = html.unescape(m.group(1))
            if not cid: raise ValueError("não achei o canal")
            f["cid"] = cid; f["site"] = f"https://www.youtube.com/channel/{cid}"
            raiz = ET.fromstring(baixar(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"))
            for e in raiz.findall("atom:entry", NS)[:10]:
                vid = e.findtext("yt:videoId", namespaces=NS); titulo = limpa(e.findtext("atom:title", namespaces=NS), 200)
                grp = e.find("media:group", NS); desc_v = ""; views = 0; thumb = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
                if grp is not None:
                    desc_v = grp.findtext("media:description", namespaces=NS) or ""
                    st = grp.find("media:community/media:statistics", NS)
                    if st is not None: views = int(st.get("views") or 0)
                link = (e.find("atom:link", NS).get("href") if e.find("atom:link", NS) is not None else f"https://www.youtube.com/watch?v={vid}")
                short = "/shorts/" in link or "#shorts" in (titulo + desc_v).lower()
                novos.append({"id": "v" + vid, "fonte": fid, "tipo": "video", "titulo": titulo, "link": link, "img": thumb, "videoId": vid,
                              "ts": ts_rss(e.findtext("atom:published", namespaces=NS) or ""), "resumo": limpa(desc_v, 180), "views": views, "short": short,
                              "tickers": sorted(set(TICK.findall(titulo + " " + desc_v)))[:6]})
        f["ok"] = bool(novos)
        if not novos: f["erro"] = "sem itens"
    except Exception as e:
        f["erro"] = str(e)[:160]; print(nome, "falhou:", e)
        novos = itens_old.get(fid, [])
    print(f"{nome}: {len(novos)} itens")
    fontes.append({k: v for k, v in f.items() if k != "end" or f["tipo"] == "canal"})
    itens.extend(novos)
    time.sleep(0.5)

# mercado: Ibovespa e IFIX pela B3, Selic pelo Banco Central
mercado = antigo.get("mercado", {})
for k, sym in (("ibov", "IBOV"), ("ifix", "IFIX")):
    try:
        q = json.loads(baixar(f"https://cotacao.b3.com.br/mds/api/v1/instrumentQuotation/{sym}"))["Trad"][0]["scty"]["SctyQtn"]
        mercado[k] = {"v": float(q["curPrc"]), "var": round(float(q.get("prcFlcn") or 0), 2)}
    except Exception as e: print(sym, "falhou:", e)
try:
    x = json.loads(baixar("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"))[0]
    mercado["selic"] = {"v": float(str(x["valor"]).replace(",", ".")), "d": x["data"]}
except Exception as e: print("Selic falhou:", e)

itens.sort(key=lambda x: -x["ts"])
agora = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
json.dump({"atualizado": agora, "fontes": fontes, "itens": itens, "mercado": mercado},
          open(saida, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("conteúdo:", len(fontes), "fontes,", len(itens), "itens")
