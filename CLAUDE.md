# Portfolio Évhira

> Projeto da Eliane (Évhira). Os padrões técnicos, visuais, de segurança e de copy
> vivem na base de conhecimento, e quem os carrega é o GENESIS, sob demanda:
> `/genesis-iniciar` para trabalho novo, `/genesis-continuar` para retomar.
> Este arquivo descreve só o que é específico DESTE projeto.

## STACK TRAVADA

- **Framework:** Flask 3.1 + Jinja2 (mínimo, 1 rota)
- **Tipo:** Pagina_Web_Simples (regime WEB, segurança obrigatória, leve por não ter login nem estado)
- **Banco:** nenhum (a página não guarda dado; o CTA vai pro WhatsApp)
- **Python:** 3.13
- **PROIBIDO:** Streamlit, Gradio, FastAPI, Django, Dash, NiceGUI, Flet

## Identidade visual deste projeto

Token: `--accent` (e -hover, -escura, -suave, -soft, -sombra, -texto), em `static/css/tokens.css`
Cor da marca: `#C9A84C` (dourado)
Tema: escuro fixo (sem alternador), pra casar com a marca Évhira (evhira.com)
Superfícies: `--bg: #010715` (igual ao fundo do logotipo), `--surface: #0F1829`, `--text: #F5F0E8` (creme)
Fontes: Inter (base) + Sora (títulos), self-host em `static/fonts/`
Ícones: Phosphor self-host em `static/phosphor/` (pesos regular e bold). Zero CDN, zero emoji.
PROIBIDO: o hex `#C9A84C` aparecer em qualquer template
PROVA: `grep -rn "C9A84C" templates/` volta vazio

## Como rodar

```
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -r requirements.txt
python app.py             # http://127.0.0.1:5000
```

## Como publicar

PRODUÇÃO (evhira.com): versão em arquivos prontos na `public_html` da Hostinger. Gere com
`python scripts/exportar_estatico.py` e envie o conteúdo de `dist/` (a pasta `static`, o `index.html` e o `.htaccess`).
Antes de trocar, baixe um ZIP da `public_html` como backup. DNS e e-mail do domínio não são tocados.
TESTE: container no EasyPanel (Docker), build por Dockerfile a partir do GitHub `elianeamorim/portfolio-evhira`
(branch main, porta 8000, HTTPS via Traefik): https://evhira-portfolio.kbls3t.easypanel.host. Sem banco e sem estado,
não precisa de volume. `gunicorn -w 2 -b 0.0.0.0:8000 app:app` (no Dockerfile).

## Fonte da verdade

O Flask (`app.py`, `templates/`, `static/`) é a fonte. Mudou texto, imagem ou CSS: gere `dist/` de novo e republique nos dois lugares.

## Módulos

- `app.py`: único .py da raiz. Guarda o número de WhatsApp e o e-mail do CTA (constantes no topo). Rota `/` (a página) e `/health`,
  mais `after_request` com os headers de segurança.

## Convenções deste projeto

- Página ÚNICA (landing). Navegação por âncoras no topo, sem sidebar.
- CTA = link direto pro WhatsApp (`https://wa.me/<numero>`). Sem formulário, sem banco, sem login.
- Copy sem travessão e sem marketês (voz consultor/professor). Cor só via `var(--accent)`.
- A demonstração principal é o app de prospeção (já pronto), mostrado por print/vídeo que a Eliane fornece.
- Todo avanço de fase passa pela skill `genesis-continuar`. Nada é construído direto do plano.

## Ritmo dos ajudantes

Paralelismo: auto

## Armadilhas

- Nenhum hex da marca (`#C9A84C`) pode aparecer em template: cor só por `var(--accent)`.
- Sem Google Fonts nem CDN de ícone: tudo self-host em `static/`.
- Em 08/10/2026 as Fases 1 e 2 foram feitas fora da skill e refeitas do zero a pedido da Eliane.
