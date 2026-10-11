# Pablo Finanças

App pessoal de finanças em formato de rede social. Cada personalidade tem foto e perfil, e cada movimentação vira um post com foto.
Funciona offline, instala no celular como app e guarda tudo **só no seu aparelho**. Não depende do Claude, de servidor nem de conta.

## O que tem nesta versão (etapa 1)

- Personalidades: crie quantas quiser, com foto (recorte com zoom e arraste), cor do anel, bio, limite mensal de gastos e saldo inicial.
- Posts com foto: cada entrada, gasto ou transferência pode levar uma foto. Sem foto, o app desenha os rastros de luz.
- Perfil como álbum: a grade de cada personalidade mostra as fotos dos posts do mês.
- Extrato com busca e filtro, aviso quando uma personalidade passa de 80% do limite.
- Ajustes: reserva de emergência em meses (cada pessoa define a sua) e backup.

## Arquivos

| Arquivo | Pra que serve |
|---|---|
| `index.html` | O app inteiro: telas, estilo e lógica |
| `manifest.webmanifest` | Nome, cores e ícones para instalar como app |
| `sw.js` | Faz o app abrir sem internet |
| `icon-*.png` | Ícones do app |

---

## Passo a passo: publicar no GitHub pelo computador

Você não precisa instalar nada nem usar terminal. Tudo é feito pelo site.

### 1. Prepare os arquivos
1. Baixe o `pablo-financas.zip`.
2. Clique com o botão direito nele → **Extrair tudo** (Windows) ou dê dois cliques (Mac).
3. Você vai ter uma pasta com 7 arquivos. Deixe essa pasta aberta.

### 2. Crie sua conta no GitHub
1. Entre em **github.com** e clique em **Sign up**.
2. Use seu e-mail, crie uma senha e escolha um **nome de usuário**. Ele vai aparecer no endereço do app (ex.: `pabloalves.github.io`), então escolha um que você goste.
3. Confirme o código que chega no e-mail.

### 3. Crie o repositório (a "pasta" do app no GitHub)
1. Logado, clique no **+** no canto superior direito → **New repository**.
2. Em **Repository name**, escreva: `financas`
3. Marque **Public**.
   - Fica tranquilo: o que fica público é só o **código** do app. **Suas movimentações e fotos nunca vão pro GitHub**, elas ficam só no celular.
4. Deixe o resto como está e clique em **Create repository**.

### 4. Envie os arquivos
1. Na página que abriu, procure o link **uploading an existing file** e clique nele.
2. Arraste **os 7 arquivos** de dentro da pasta (não a pasta em si) para a área pontilhada.
3. Espere carregar todos. Embaixo, em **Commit changes**, clique no botão verde **Commit changes**.

### 5. Ligue o GitHub Pages (o "servidor" grátis)
1. No topo do repositório, clique em **Settings** (ícone de engrenagem).
2. No menu da esquerda, clique em **Pages**.
3. Em **Source**, escolha **Deploy from a branch**.
4. Em **Branch**, escolha **main**, a pasta **/ (root)**, e clique em **Save**.
5. Espere de 1 a 3 minutos e atualize a página. Vai aparecer: **"Your site is live at https://SEU-USUARIO.github.io/financas/"**.

Esse é o endereço do seu app.

### 6. Instale no celular
1. Mande o endereço pra você mesmo (WhatsApp, e-mail) e abra no celular.
2. **Android (Chrome):** menu ⋮ → **Instalar app** (ou *Adicionar à tela inicial*).
3. **iPhone (Safari):** botão Compartilhar → **Adicionar à Tela de Início**.

Pronto: ícone próprio, tela cheia, funciona sem internet.

---

## Atualizar o app quando sair versão nova

1. No repositório, clique em **Add file → Upload files**.
2. Arraste os arquivos novos. O GitHub substitui os antigos com o mesmo nome.
3. Clique em **Commit changes**.
4. No celular, feche o app e abra de novo (às vezes precisa fazer isso duas vezes). Seus dados continuam lá.

Cada versão nova do `sw.js` já vem com o número de versão aumentado. É isso que avisa o celular que tem atualização.

## Seus dados

- Ficam no armazenamento do navegador do celular.
- **Faça backup:** Ajustes → *Exportar backup* gera um arquivo `.json` com tudo, fotos inclusas. Salve no Drive.
- Trocou de celular ou limpou os dados do navegador? Ajustes → *Importar backup* restaura tudo.
- Desinstalar o app ou limpar os dados do site **apaga** tudo. Por isso o backup importa.
- O app no celular e o app no PC são separados: cada um guarda os próprios dados. Juntar os dois é a Fase 2 (nuvem).

## Etapa 2 (esta versão)

- Robôs que postam sozinhos quando você abre o app: @câmbio (dólar do dia), @lembretes (datas que você cadastra), @resumo (toda segunda, a semana anterior) e @lembranças (posts com foto de 1 semana, 1 mês e 1 ano atrás).
- Coração no topo: notificações dos robôs, com bolinha quando tem novidade.
- Ajustes: ligar e desligar cada robô e cadastrar lembretes. O botão "Registrar agora" abre o post já preenchido.
- Editar post (⋯ → Editar) e aviso quando uma personalidade ficaria com saldo negativo.

## Robôs como perfis (esta versão)

- Aba **Explorar** (lupa na barra de baixo): os robôs disponíveis, com botão Seguir.
- **Perfil de cada robô:** bio, "o que eu faço", "quando eu posto", "o que eu vejo dos seus dados" e a grade com o histórico de posts.
- **Sininho** em cada robô seguido: Todas, Só as importantes ou Nenhuma. Só o que você escolher aparece no coração.
- **Menos barulho:** o @câmbio só posta quando o dólar mexe 0,5% ou mais (ou uma vez por semana); o @lembranças traz no máximo uma lembrança por dia.
- **Ajustes** agora fica na engrenagem do topo da aba Perfis.

## Próximas etapas

3. Carteira de FIIs no Pablo Rico e o @fii
4. Projeção ("e se?"), lista de desejos e @poderdecompra

Fase 2: dados e fotos na nuvem (Supabase), contas, ver o perfil de um amigo e conversar no app.
