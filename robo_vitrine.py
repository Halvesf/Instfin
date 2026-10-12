# Robô da vitrine do @poderdecompra.
# Monta o vitrine.json ao lado do index.html, uma vez por dia:
#   - carros e motos com preço da Tabela FIPE (api pública parallelum)
#   - preço médio do m² por cidade pelo índice FipeZap (relatório mensal em PDF)
#   - fotos livres do Wikimedia Commons
#   - itens de referência (eletrônicos, viagens, experiências) com preço aproximado
import json, os, re, time, unicodedata, urllib.request, urllib.parse, datetime as dt

UA = {"User-Agent": "PabloFinancas/1.0 (app pessoal; github.com/Halvesf/Instfin)", "Accept": "*/*"}
def baixar(url, timeout=25, tent=3):
    err = None
    for i in range(tent):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read()
        except Exception as e:
            err = e; time.sleep(1.5 + i * 3)
    raise err
def jget(url): return json.loads(baixar(url).decode("utf-8"))
def norm(s): return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
def slug(s): return re.sub(r"[^a-z0-9]+", "-", norm(s)).strip("-")
def reais(txt): return int(round(float(re.sub(r"[^\d,]", "", txt).replace(",", ".")) * 100))

pasta = "."
for raiz, dirs, arqs in os.walk("."):
    if ".git" in raiz: continue
    if "index.html" in arqs and "pablo-financas" in open(os.path.join(raiz, "index.html"), encoding="utf-8", errors="ignore").read():
        pasta = raiz; break
saida = os.path.join(pasta, "vitrine.json")
antigo = {}
if os.path.exists(saida):
    try: antigo = json.load(open(saida, encoding="utf-8"))
    except Exception: antigo = {}
if antigo.get("atualizado") and os.environ.get("FORCAR_VITRINE") != "1":
    idade = dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(antigo["atualizado"].replace("Z", "+00:00"))
    if idade < dt.timedelta(hours=20):
        print("vitrine atualizada há", idade, "- nada a fazer"); raise SystemExit(0)
velhos = {it["id"]: it for it in antigo.get("itens", [])}

# ---------- catálogo ----------
# (tipo FIPE, marca, palavras do modelo, ano, termo da foto)
VEICULOS = [
    ("carros", "Fiat", "Mobi Like", 2024, "Fiat Mobi"),
    ("carros", "Hyundai", "HB20 Comfort 1.0", 2023, "Hyundai HB20 2020"),
    ("carros", "Chevrolet", "Onix LT 1.0", 2024, "Chevrolet Onix 2020"),
    ("carros", "VolksWagen", "T-Cross Highline", 2023, "Volkswagen T-Cross"),
    ("carros", "Honda", "Civic Touring", 2021, "Honda Civic 2020 sedan"),
    ("carros", "Toyota", "Corolla XEi 2.0", 2023, "Toyota Corolla E210 sedan"),
    ("carros", "Jeep", "Compass Limited", 2023, "Jeep Compass 2022"),
    ("carros", "Toyota", "Hilux SRV", 2022, "Toyota Hilux 2021"),
    ("carros", "BMW", "320i", 2012, "BMW 3 Series E90 320i"),
    ("carros", "BMW", "320i M Sport", 2022, "BMW 3 Series G20"),
    ("carros", "Mercedes-Benz", "C-200", 2020, "Mercedes-Benz C-Class W205"),
    ("carros", "Porsche", "911 Carrera", 2020, "Porsche 911 992 Carrera"),
    ("motos", "Honda", "CG 160 Fan", 2024, "Honda CG 160"),
    ("motos", "Yamaha", "MT-03", 2024, "Yamaha MT-03"),
    ("motos", "BMW", "R 1250 GS", 2022, "BMW R1250GS"),
    ("motos", "Harley-Davidson", "Fat Boy", 2020, "Harley-Davidson Fat Boy"),
]
# itens de referência: preço aproximado em reais (o app mostra como "referência")
REFERENCIA = [
    ("eletronico", "iPhone Pro (modelo mais novo)", 9500, "iPhone 15 Pro", "iphone pro"),
    ("eletronico", "Samsung Galaxy S Ultra", 7500, "Samsung Galaxy S24 Ultra", "galaxy s ultra"),
    ("eletronico", "MacBook Air", 9000, "MacBook Air M2", "macbook air"),
    ("eletronico", "PlayStation 5", 4000, "PlayStation 5 console", "playstation 5"),
    ("eletronico", "Notebook gamer", 7000, "gaming laptop", "notebook gamer"),
    ("eletronico", "Fone com cancelamento de ruído", 1800, "Sony WH-1000XM5 headphones", "fone cancelamento de ruido"),
    ("eletrodomestico", "Smart TV 65 polegadas", 4000, "65 inch television living room", "smart tv 65"),
    ("eletrodomestico", "Geladeira inverter frost free", 4500, "refrigerator kitchen stainless", "geladeira inverter"),
    ("eletrodomestico", "Air fryer", 500, "air fryer", "air fryer"),
    ("eletrodomestico", "Máquina lava e seca", 4000, "washing machine dryer", "lava e seca"),
    ("viagem", "Mochilão pela Europa · 15 dias", 18000, "Eiffel Tower Paris", "Paris"),
    ("viagem", "Japão · 15 dias", 25000, "Tokyo Shibuya crossing", "Tóquio"),
    ("viagem", "Orlando e Disney · 10 dias", 20000, "Cinderella Castle Magic Kingdom", "Orlando"),
    ("viagem", "Nordeste · 7 dias", 4500, "Porto de Galinhas beach", "Recife"),
    ("viagem", "Buenos Aires · 5 dias", 4000, "Buenos Aires Obelisco", "Buenos Aires"),
    ("experiencia", "Show internacional · pista premium", 1200, "concert crowd stage lights", ""),
    ("experiencia", "Jantar num restaurante estrelado", 1500, "fine dining plate restaurant", ""),
    ("experiencia", "Fim de semana em Campos do Jordão", 2500, "Campos do Jordão", ""),
]
# casas: o preço sai do m² da cidade escolhida no app
CASAS = [("casa", "Apê de 50 m²", 50, "apartment building Brazil"), ("casa", "Apê de 70 m²", 70, "apartment balcony building"),
         ("casa", "Casa de 120 m²", 120, "house Brazil residential street")]
CIDADES = [("São Paulo", "SP"), ("São Bernardo do Campo", "SP"), ("Santo André", "SP"), ("São Caetano do Sul", "SP"), ("Diadema", "SP"),
           ("Guarulhos", "SP"), ("Osasco", "SP"), ("Campinas", "SP"), ("Santos", "SP"), ("São José dos Campos", "SP"), ("Sorocaba", "SP"),
           ("Ribeirão Preto", "SP"), ("Rio de Janeiro", "RJ"), ("Niterói", "RJ"), ("Belo Horizonte", "MG"), ("Curitiba", "PR"),
           ("Florianópolis", "SC"), ("Porto Alegre", "RS"), ("Brasília", "DF"), ("Goiânia", "GO"), ("Salvador", "BA"), ("Recife", "PE"),
           ("Fortaleza", "CE"), ("Manaus", "AM"), ("Belém", "PA"), ("Vitória", "ES"), ("João Pessoa", "PB"), ("Natal", "RN"), ("Maceió", "AL")]

def foto(termo, velho=""):
    if velho or not termo: return velho
    try:
        q = urllib.parse.urlencode({"action": "query", "generator": "search", "gsrsearch": "filetype:bitmap " + termo, "gsrnamespace": 6, "gsrlimit": 6,
                                    "prop": "imageinfo", "iiprop": "url|size", "iiurlwidth": 900, "format": "json"})
        j = jget("https://commons.wikimedia.org/w/api.php?" + q)
        pags = sorted((j.get("query") or {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
        for p in pags:
            ii = (p.get("imageinfo") or [{}])[0]
            if ii.get("width", 0) >= 600 and ii.get("thumburl"): return ii["thumburl"]
    except Exception as e: print("foto falhou:", termo, e)
    return ""

itens = []
# ---------- FIPE ----------
fipe = "https://parallelum.com.br/fipe/api/v1"
marcas_cache, mes_fipe = {}, ""
for tipo, marca, modelo, ano, termo in VEICULOS:
    iid = slug(f"{marca}-{modelo}-{ano}")
    old = velhos.get(iid, {})
    try:
        if tipo not in marcas_cache: marcas_cache[tipo] = jget(f"{fipe}/{tipo}/marcas")
        mk = next(m for m in marcas_cache[tipo] if norm(marca) in norm(m["nome"]))
        mods = jget(f"{fipe}/{tipo}/marcas/{mk['codigo']}/modelos")["modelos"]
        toks = norm(modelo).split()
        cands = sorted([m for m in mods if all(t in norm(m["nome"]) for t in toks)], key=lambda m: len(m["nome"]))
        if not cands: raise ValueError("modelo não achado")
        anos = None
        for md in cands[:6]:
            a = jget(f"{fipe}/{tipo}/marcas/{mk['codigo']}/modelos/{md['codigo']}/anos")
            alvo = [x for x in a if x["codigo"].startswith(f"{ano}-")]
            if alvo: anos = (md, alvo[0]); break
            time.sleep(0.4)
        if not anos: raise ValueError("ano não achado")
        md, an = anos
        v = jget(f"{fipe}/{tipo}/marcas/{mk['codigo']}/modelos/{md['codigo']}/anos/{an['codigo']}")
        mes_fipe = (v.get("MesReferencia") or "").strip()
        nome = f"{v.get('Marca', marca)} {modelo} {ano}"
        itens.append({"id": iid, "cat": "carro" if tipo == "carros" else "moto", "nome": nome, "detalhe": v.get("Modelo", md["nome"]),
                      "preco": reais(v["Valor"]), "fonte": "Tabela FIPE · " + mes_fipe, "img": foto(termo, old.get("img", "")),
                      "fipe": {"tipo": tipo, "marca": mk["codigo"], "modelo": md["codigo"], "ano": an["codigo"]},
                      "links": [["Ver anúncios na OLX", "https://www.olx.com.br/autos-e-pecas?q=" + urllib.parse.quote(f"{marca} {modelo} {ano}")],
                                ["Ver na Webmotors", f"https://www.webmotors.com.br/{'carros' if tipo == 'carros' else 'motos'}/estoque/{slug(marca.split()[-1])}"]]})
        print("FIPE ok:", nome, v["Valor"])
    except Exception as e:
        print("FIPE falhou:", marca, modelo, ano, e)
        if old: itens.append(old)
    time.sleep(0.6)

# ---------- referência ----------
for cat, nome, preco, termo, busca in REFERENCIA:
    iid = slug(nome); old = velhos.get(iid, {})
    links = []
    if cat in ("eletronico", "eletrodomestico"): links.append(["Ver no Mercado Livre", "https://lista.mercadolivre.com.br/" + slug(busca)])
    if cat == "viagem": links.append(["Pesquisar passagens", "https://www.google.com/travel/flights?q=" + urllib.parse.quote(f"voos de São Paulo para {busca}")])
    itens.append({"id": iid, "cat": cat, "nome": nome, "preco": preco * 100, "fonte": "preço de referência (aproximado)", "ref": True,
                  "img": foto(termo, old.get("img", "")), "links": links})

# ---------- casas (m² por cidade, FipeZap) ----------
m2 = dict(antigo.get("m2", {}))
hoje = dt.date.today()
for k in range(0, 5):
    ano, mes = hoje.year, hoje.month - k
    while mes <= 0: mes += 12; ano -= 1
    url = f"https://downloads.fipe.org.br/indices/fipezap/fipezap-{ano}{mes:02d}-residencial-venda.pdf"
    try:
        pdf = baixar(url, tent=1)
        import io
        from pypdf import PdfReader
        texto = "\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(pdf)).pages)
        achou = 0
        for cidade, uf in CIDADES:
            m = re.search(re.escape(cidade) + r"(?:\s*\(" + uf + r"\))?[^\n\d]{0,12}(\d{1,2}\.\d{3})\b", texto)
            if m:
                v = int(m.group(1).replace(".", ""))
                if 2000 <= v <= 30000: m2[cidade] = {"v": v, "uf": uf, "mes": f"{mes:02d}/{ano}"}; achou += 1
        print("FipeZap", f"{mes:02d}/{ano}:", achou, "cidades")
        if achou: break
    except Exception as e:
        print("FipeZap", f"{mes:02d}/{ano}", "indisponível:", str(e)[:80])
for cat, nome, area, termo in CASAS:
    iid = slug(nome); old = velhos.get(iid, {})
    itens.append({"id": iid, "cat": cat, "nome": nome, "m2": area, "fonte": "FipeZap · preço médio do m²", "img": foto(termo, old.get("img", ""))})

agora = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
json.dump({"atualizado": agora, "fipeMes": mes_fipe, "m2": m2, "cidades": [{"nome": c, "uf": u} for c, u in CIDADES], "itens": itens},
          open(saida, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("vitrine:", len(itens), "itens,", len(m2), "cidades com m²")
