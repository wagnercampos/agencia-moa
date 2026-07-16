# _scripts — geração das páginas de nicho

## build_nichos.py

Gera as páginas de nicho do site (médicos, restaurantes, hotéis) reusando o **casco**
do `index.html`, com **miolo próprio** para cada nicho.

```bash
cd ~/Documents/"Criador de Sites/agencia-moa"
python3 _scripts/build_nichos.py
```

É **idempotente**: rodar de novo gera arquivos idênticos. Rode sempre que mexer no
`index.html` (nav, rodapé, CSS, schema da home) para as páginas de nicho herdarem a mudança.

### Como funciona

- Corta o `index.html` por **marcador**, nunca por número de linha:
  - `top` = tudo antes de `<!-- HERO -->` (head + nav + menu mobile)
  - `bottom` = de `<!-- FOOTER -->` até o fim (rodapé + WhatsApp float + scripts)
  - `clients` = entre `<!-- CLIENTS -->` e `<!-- TEAM -->` (vitrine de 30 marcas, injetada como prova social)
- Troca o SEO do head (title/description/og/canonical) e injeta schema `Service` + `FAQPage`
  (o `MarketingAgency` da home vem junto no casco → 3 blocos JSON-LD por página).
- Injeta o CSS do FAQ (usa os tokens da marca: `--orange`, `--font-display`…).
- Reescreve âncoras de seções que **não existem** na página de nicho (`#manifesto`, `#services`,
  `#clients`, `#team`, `#labs`) para `index.html#...`. Ficam locais só `#como-funciona` e `#contact`.
- **Aborta** (`sys.exit`) se um marcador ou um trecho do head não for encontrado — para nunca
  gerar página quebrada em silêncio.

### Adicionar um nicho novo

Basta acrescentar um bloco na lista `NICHOS` (slug, title, desc, hero, problema, 6 serviços,
FAQ, CTA). Depois, manualmente:

1. Link no rodapé do `index.html` (seção "Serviços") — **antes** de rodar o script, senão a
   página nova nasce com um rodapé sem ela.
2. Mesmo link no rodapé de `agencia-de-marketing-em-teresina.html` (essa é clone manual, não sai do script).
3. Entrada no `sitemap.xml` e no `llms.txt`.
4. Deploy (ver `SESSAO-*.md` em `~/Documents/Desenvolvedor/seo-moa/`).

### Regras de conteúdo (por que não é clone da home)

- Página de nicho **não pode** ser a home com o título trocado → o Google trata como
  "página-porta" (doorway page) e penaliza. Cada nicho tem dor, serviços e FAQ próprios.
- A vitrine de clientes é injetada **sem rótulo de segmento** ("quem confia na gente"),
  porque nem todo cliente da lista é do nicho da página — rotular seria erro factual no ar.
