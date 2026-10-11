// Service worker: deixa o app abrir sem internet.
// Ao mudar qualquer arquivo do app, aumente o número da versão abaixo
// para o celular baixar a versão nova.
const VERSAO = "financas-v6";
const ARQUIVOS = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "icon-maskable-512.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSAO).then(c => c.addAll(ARQUIVOS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== VERSAO).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Arquivos do app: tenta a rede primeiro (pega atualizações) e cai no cache se estiver offline.
// Fontes do Google: usa o cache primeiro.
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.hostname.includes("fonts.googleapis.com") || url.hostname.includes("fonts.gstatic.com")) {
    e.respondWith(caches.open(VERSAO).then(c => c.match(req).then(hit => hit || fetch(req).then(r => { c.put(req, r.clone()); return r; }))));
    return;
  }
  if (url.origin !== location.origin) return;
  e.respondWith(
    fetch(req).then(r => {
      const copia = r.clone();
      caches.open(VERSAO).then(c => c.put(req, copia));
      return r;
    }).catch(() => caches.match(req).then(hit => hit || caches.match("index.html")))
  );
});
