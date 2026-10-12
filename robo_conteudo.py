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
    t = re.sub(r"\s*(The post\b.*?appeared first on.*|O post\b.*?apareceu primeiro em.*)$", "", t)
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
def paragrafos(h, maxp=8, maxc=1800):
    """texto limpo em parágrafos, a partir do HTML do feed ou da página"""
    h = re.sub(r"(?is)<(script|style|figure|figcaption|aside|nav|form|iframe)[^>]*>.*?</\1>", " ", h or "")
    ps, total = [], 0
    for p in re.findall(r"(?is)<p[^>]*>(.*?)</p>", h):
        t = limpa(p, 1200)
        if len(t) < 40 or re.search(r"(?i)(leia também|leia mais|assine|newsletter|cookies|whatsapp|siga o |clique aqui)", t): continue
        ps.append(t); total += len(t)
        if len(ps) >= maxp or total >= maxc: break
    return ps
UNID = {"second": 1, "segundo": 1, "minute": 60, "minuto": 60, "hour": 3600, "hora": 3600, "day": 86400, "dia": 86400,
        "week": 604800, "semana": 604800, "month": 2592000, "mês": 2592000, "mes": 2592000, "meses": 2592000, "year": 31536000, "ano": 31536000}
def tempo_rel(txt):
    """'2 days ago', 'Streamed 5 hours ago', 'há 2 dias', '3 semanas atrás' -> timestamp; None se não achar"""
    t = (txt or "").lower()
    m = re.search(r"(\d+)\s+(second|minute|hour|day|week|month|year)s?\s+ago", t) or \
        re.search(r"(?:há\s+)?(\d+)\s+(segundo|minuto|hora|dia|semana|meses|mês|mes|ano)s?(?:\s+atrás)?", t)
    if not m: return None
    return int((time.time() - int(m.group(1)) * UNID[m.group(2)]) * 1000)
def views_txt(txt):
    t = (txt or "")
    m = re.search(r"([\d.,]+)\s*([KMB]?)\s+views", t)
    if m:
        n = float(m.group(1).replace(",", "")) if not m.group(2) else float(m.group(1).replace(",", "."))
        return int(n * {"": 1, "K": 1e3, "M": 1e6, "B": 1e9}[m.group(2)])
    m = re.search(r"([\d.,]+)\s*(mil|mi|bi)?\s*(?:de\s+)?visualiza", t)
    if m:
        n = float(m.group(1).replace(".", "").replace(",", ".")) if m.group(2) else float(m.group(1).replace(".", "").replace(",", ""))
        return int(n * {None: 1, "mil": 1e3, "mi": 1e6, "bi": 1e9}[m.group(2)])
    return 0
AMOSTRA = []
def videos_da_pagina(url):
    """lê a aba Vídeos do canal (quando o feed RSS do YouTube falha)"""
    h = baixar(url + ("&" if "?" in url else "?") + "hl=en&gl=US").decode("utf-8", "ignore")
    m = re.search(r"var ytInitialData\s*=\s*(\{.*?\});\s*</script>", h, re.S) or re.search(r"ytInitialData\"\]\s*=\s*(\{.*?\});", h, re.S)
    if not m: raise ValueError("página do canal sem lista de vídeos")
    dados = json.loads(m.group(1)); out = []
    def txt(o):
        if isinstance(o, dict):
            if "simpleText" in o: return o["simpleText"]
            if "runs" in o: return "".join(r.get("text", "") for r in o["runs"])
            if "content" in o: return o["content"]
        return ""
    def textos(o, acc=None):
        acc = [] if acc is None else acc
        if isinstance(o, dict):
            for k, x in o.items():
                if k in ("content", "simpleText", "text", "label") and isinstance(x, str) and len(x) < 120: acc.append(x)
                else: textos(x, acc)
        elif isinstance(o, list):
            for x in o: textos(x, acc)
        return acc
    def anda(o):
        if len(out) >= 12: return
        if isinstance(o, dict):
            if "videoRenderer" in o:
                v = o["videoRenderer"]; tudo = " | ".join(textos(v))
                out.append({"vid": v.get("videoId"), "titulo": txt(v.get("title")), "quando": txt(v.get("publishedTimeText")) + " | " + tudo, "views": txt(v.get("viewCountText")) + " | " + tudo, "desc": txt(v.get("descriptionSnippet"))})
                if len(AMOSTRA) < 1: AMOSTRA.append(tudo[:600])
                return
            if "lockupViewModel" in o:
                v = o["lockupViewModel"]
                if v.get("contentType", "").endswith("VIDEO"):
                    md = (v.get("metadata") or {}).get("lockupMetadataViewModel") or {}
                    partes = []
                    for row in (((md.get("metadata") or {}).get("contentMetadataViewModel") or {}).get("metadataRows") or []):
                        for p in row.get("metadataParts") or []: partes.append(txt(p.get("text")))
                    tudo = " | ".join(partes + textos(v))
                    out.append({"vid": v.get("contentId"), "titulo": txt(md.get("title")), "quando": tudo, "views": tudo, "desc": ""})
                    if len(AMOSTRA) < 1: AMOSTRA.append(tudo[:600])
                return
            for x in o.values(): anda(x)
        elif isinstance(o, list):
            for x in o: anda(x)
    anda(dados)
    return [v for v in out if v["vid"]]
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
texto_cache = {it["link"]: it.get("texto") for it in antigo.get("itens", []) if it.get("texto")}

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
                              "link": link, "img": img, "ts": ts_rss(it.findtext("pubDate") or ""), "resumo": limpa(desc_h or cont, 220), "tickers": tks, "texto": paragrafos(cont) or texto_cache.get(link) or []})
            # da página: imagem (og:image) e primeiros parágrafos, para as mais novas que vieram sem
            for n in [x for x in novos if not x["img"] or not x["texto"]][:6]:
                try:
                    h = baixar(n["link"], timeout=12, tent=1).decode("utf-8", "ignore")
                    if not n["img"]:
                        m = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', h) or re.search(r'<meta[^>]+content="([^"]+)"[^>]+property="og:image"', h)
                        if m: n["img"] = html.unescape(m.group(1))
                    if not n["texto"]:
                        corpo = re.search(r"(?is)<article[^>]*>(.*?)</article>", h)
                        n["texto"] = paragrafos(corpo.group(1) if corpo else h, maxp=5, maxc=1000)
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
            try: raiz = ET.fromstring(baixar(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}", tent=1))
            except Exception as e_rss:
                print(nome, "feed do YouTube falhou (", e_rss, "), lendo a página do canal")
                raiz = None
                ant_ts = {x["id"]: x["ts"] for x in itens_old.get(fid, []) if x.get("tsOk")}
                for pos, v in enumerate(videos_da_pagina(f"https://www.youtube.com/channel/{cid}/videos")[:10]):
                    vid_id = "v" + v["vid"]; t_rel = tempo_rel(v["quando"])
                    ts_v = t_rel or ant_ts.get(vid_id) or int((time.time() - 86400 * 3 * (pos + 1)) * 1000)
                    novos.append({"id": vid_id, "fonte": fid, "tipo": "video", "titulo": limpa(v["titulo"], 200), "link": f"https://www.youtube.com/watch?v={v['vid']}", "tsOk": bool(t_rel or vid_id in ant_ts),
                                  "img": f"https://i.ytimg.com/vi/{v['vid']}/hqdefault.jpg", "videoId": v["vid"], "ts": ts_v, "resumo": limpa(v["desc"], 180),
                                  "views": views_txt(v["views"]), "short": False, "tickers": sorted(set(TICK.findall(v["titulo"])))[:6]})
            for e in (raiz.findall("atom:entry", NS)[:10] if raiz is not None else []):
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
json.dump({"atualizado": agora, "fontes": fontes, "itens": itens, "mercado": mercado, "_amostraVideo": AMOSTRA[:1]},
          open(saida, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("conteúdo:", len(fontes), "fontes,", len(itens), "itens")
