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
| `tickers.txt` | Lista dos FIIs e ações que o robô de cotações acompanha |
| `robo-cotacoes.yml` | O robô de cotações. **Não suba este arquivo**: copie o conteúdo dele (passo a passo abaixo) |

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

## O plano e os carrosséis (esta versão)

- **Configurar meu dinheiro:** assistente de 10 passos (saldos de hoje, renda, benefícios, divisão, contas fixas com data de fim, compromissos futuros, eventos do ano, metas e robôs). Abre pelo aviso no Início ou em Perfis → engrenagem → Meu plano.
- **Recomeçar do zero:** no passo 1 do assistente, com opção de exportar backup antes.
- **Posts vivos em carrossel:** @meumês, @contas, @reserva e @horizonte atualizam sozinhos e fecham no fim do período, virando o arquivo mês a mês no perfil de cada robô.
- **@holerite:** compara cada pagamento com o previsto e oferece atualizar a previsão quando a renda muda.
- O que tem data anterior ao dia em que você informou os saldos aparece como "já no saldo" e não conta de novo.

## Livre para gastar (esta versão)

- O @meumês abre com **Livre para gastar hoje**: o quanto dá para gastar sem ficar no vermelho em nenhum dia até o fim do mês seguinte e sem mexer na reserva.
- Slide **Seu saldo dia a dia**: gráfico em degraus com os dias de entrada e o dia mais apertado.
- Novo passo no assistente: **Este mês já começou** — marque o que já foi pago ou recebido antes de começar a usar o app.

## Investimentos (etapa 3)

- Cada personalidade tem **caixa** (dinheiro disponível) e **carteira** (investimentos). Perfil → aba **Carteira**.
- **Renda fixa** (CDB, LCI, LCA, Tesouro Selic, caixinha): rendimento estimado por dia útil com o CDI do Banco Central, IR regressivo, Aplicar, Resgatar e **Conferir** (digite o saldo do banco e a diferença vira rendimento).
- **FIIs e ações:** cotas, preço médio, cotação e proventos pela brapi (cole o token em Ajustes → Investimentos), Comprar, Vender e Registrar provento.
- **Importar da B3:** baixe o extrato de Movimentação (e, se quiser, o de Posição) na Área do Investidor e importe na aba Carteira.
- Robôs **@rendimentos** e **@fii**. O @reserva passa a contar a carteira, e o @horizonte inclui os rendimentos.

## Robô de cotações (sem token, tudo automático)

Um robô gratuito do próprio GitHub roda de hora em hora nos dias úteis (10h às 18h) e uma vez toda noite. Ele busca a cotação e os proventos dos seus FIIs e o CDI, e salva tudo no arquivo `cotacoes.json`, no seu repositório. O app lê esse arquivo sozinho.

### Ligar o robô (uma vez só, pelo computador)
1. Suba os arquivos do app como sempre, **incluindo o `tickers.txt`**, na mesma pasta do `index.html`.
2. Na página inicial do repositório, clique em **Add file → Create new file**.
3. No nome do arquivo, digite exatamente: `.github/workflows/cotacoes.yml`. Ao digitar cada `/`, o GitHub cria a pasta sozinho.
4. Abra o `robo-cotacoes.yml` no Bloco de Notas, copie tudo (Ctrl+A, Ctrl+C) e cole na área grande do GitHub.
5. Clique em **Commit changes** duas vezes.
6. Vá em **Settings → Actions → General**. Lá embaixo, em *Workflow permissions*, marque **Read and write permissions** e clique em **Save**.
7. Clique na aba **Actions** (no topo) → **Cotações** (à esquerda) → **Run workflow** → **Run workflow**.
8. Espere uns 2 minutos até aparecer o ✓ verde. O `cotacoes.json` aparece no repositório.
9. No app: Perfis → engrenagem → Investimentos → **Testar conexões**. Tem que aparecer ✓ Robô do GitHub.

### Incluir um FII ou ação novo
- No app: Ajustes → Investimentos → **Editar lista de ativos**. Isso abre o `tickers.txt` no GitHub.
- Escreva o código numa linha nova (ex.: `HGLG11`) e clique em **Commit changes**. O robô roda sozinho e em poucos minutos a cotação chega.

### Bom saber
- A cotação vem da própria B3 (com Yahoo e Fundamentus de reserva) e os proventos vêm do Fundamentus, com data-com, data de pagamento e valor por cota. Nenhuma dessas fontes é oficialmente garantida: se uma parar, o app avisa qual ativo ficou sem cotação.
- O repositório é público, então a **lista de códigos** do `tickers.txt` fica visível. Quantidades, valores e o resto dos seus dados continuam só no celular.
- Se o app mostrar "Parado desde…", entre em **Actions → Cotações** e veja se o GitHub desativou o robô (ele faz isso em repositórios sem movimento por 60 dias). Se tiver o botão **Enable workflow**, clique nele.
- O token da brapi virou opcional.

## Quando os dados não aparecem

Ajustes → Investimentos → **Testar conexões** mostra o que funcionou e o que falhou:
- **Robô do GitHub:** se der ✕, confira os passos de "Ligar o robô" e se a última execução em Actions ficou verde.
- **CDI do Banco Central:** se falhar, preencha o CDI manual logo abaixo. Sem CDI a renda fixa fica em R$ 0,00.
- **Cotação:** "token recusado" significa token errado ou incompleto.
- **Proventos:** se o plano grátis da brapi não liberar, registre o último provento do FII e o app estima os próximos a partir dele.
- A renda fixa começa a render no próximo dia útil depois do cadastro ou da última conferência.

## Próximas etapas

4. Projeção ("e se?"), lista de desejos e @poderdecompra

Fase 2: dados e fotos na nuvem (Supabase), contas, ver o perfil de um amigo e conversar no app.
