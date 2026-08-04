#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builder do BLOG da Agência MOA.
Reaproveita o casco visual do ../index.html (style + nav + footer), converte cada
markdown de blog/_posts/<slug>.md em uma página de artigo com JSON-LD (Article +
FAQPage + BreadcrumbList), monta a listagem blog/index.html, e atualiza ../sitemap.xml
e ../llms.txt.

Uso: python3 build_blog.py
Adicionar post novo: crie blog/_posts/<slug>.md + uma entrada em blog/posts.json, rode de novo.
Idempotente.
"""
import os, re, json, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # .../agencia-moa
SITE = "https://agenciamoa.com.br"
WHATS = "5588988575422"
BLOG_DESC = ("Artigos práticos sobre Google, tráfego pago, presença digital e "
             "marketing para pequenas empresas. Conteúdo direto ao ponto, feito pela Agência MOA.")

# ---------- extrair casco do index.html ----------
with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
    INDEX = f.read()

def grab(pattern, src, name):
    m = re.search(pattern, src, re.S | re.I)
    if not m:
        raise SystemExit(f"ERRO: não achei {name} no index.html")
    return m.group(0)

BASE_STYLE = grab(r"<style>.*?</style>", INDEX, "<style>")
NAV        = grab(r'<nav[^>]*id="navbar".*?</nav>', INDEX, "<nav>")
FOOTER     = grab(r"<footer.*?</footer>", INDEX, "<footer>")
FONTS      = grab(r'<link[^>]+fonts.googleapis[^>]+>', INDEX, "google fonts link")
PRECONNECT = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
              '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')

def to_abs(fragment):
    """Reescreve links/asset relativos para a raiz do site (as páginas ficam em /blog/)."""
    def fix(m):
        attr, q, val = m.group(1), m.group(2), m.group(3)
        if re.match(r'^(https?:|/|#|mailto:|tel:|javascript:|data:)', val):
            if val.startswith('#'):
                val = '/' + val
            return f'{attr}={q}{val}{q}'
        if val in ('index.html', './index.html'):
            val = '/'
        else:
            val = '/' + val.lstrip('./')
        return f'{attr}={q}{val}{q}'
    return re.sub(r'(href|src)=(["\'])([^"\']*)\2', fix, fragment)

NAV_ABS = to_abs(NAV)
FOOTER_ABS = to_abs(FOOTER)

# ---------- CSS específico do blog ----------
BLOG_CSS = """
<style>
/* ==== BLOG MOA ==== */
.blog-hero { background: var(--dark); color: var(--off-white); padding: 160px 0 70px; }
.blog-hero h1 { font-family: var(--font-display); font-size: clamp(34px,5vw,60px); font-weight:600; line-height:1.05; letter-spacing:-.02em; }
.blog-hero p { max-width: 620px; margin-top: 18px; color: var(--sand); font-size: 18px; line-height:1.6; }
.post-grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(320px,1fr)); gap: 26px; padding: 70px 0 90px; }
.post-card { display:flex; flex-direction:column; background:#fff; border:1px solid #e6e5db; border-radius:16px; padding:30px; text-decoration:none; color:var(--dark); transition:transform .2s ease, box-shadow .2s ease, border-color .2s ease; }
.post-card:hover { transform: translateY(-4px); box-shadow: 0 18px 40px rgba(27,27,27,.10); border-color: var(--orange); }
.post-cat { font-size:11px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; color:var(--orange); }
.post-card h2 { font-family:var(--font-display); font-size:22px; font-weight:600; line-height:1.25; margin:14px 0 12px; letter-spacing:-.01em; }
.post-card p { font-size:15px; line-height:1.6; color:#555; flex:1; }
.post-meta { margin-top:20px; font-size:13px; color:#9a9a90; }
.post-more { margin-top:16px; font-weight:600; color:var(--red); font-size:14px; }

.article { padding: 150px 0 40px; }
.article-wrap { max-width: 760px; margin: 0 auto; }
.breadcrumb { font-size:13px; color:#9a9a90; margin-bottom:26px; }
.breadcrumb a { color:#9a9a90; text-decoration:none; } .breadcrumb a:hover { color:var(--orange); }
.article-cat { font-size:12px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; color:var(--orange); }
.article h1 { font-family:var(--font-display); font-size: clamp(30px,4.5vw,48px); font-weight:600; line-height:1.1; letter-spacing:-.02em; margin:14px 0 16px; }
.article-meta { font-size:14px; color:#9a9a90; padding-bottom:30px; border-bottom:1px solid #e6e5db; margin-bottom:36px; }
.article-body { font-size:18px; line-height:1.75; color:#2a2a2a; }
.article-body h2 { font-family:var(--font-display); font-size:26px; font-weight:600; letter-spacing:-.01em; margin:44px 0 16px; }
.article-body p { margin: 0 0 20px; }
.article-body ul, .article-body ol { margin: 0 0 24px; padding-left: 24px; }
.article-body li { margin-bottom: 10px; }
.article-body strong { color: var(--dark); }
.quick-answer { background:#eff6f6; border-left:4px solid var(--teal); border-radius:0 12px 12px 0; padding:20px 24px; margin:0 0 32px; font-size:17px; line-height:1.65; }
.quick-answer strong { color: var(--brown); }
.faq { margin-top: 20px; }
.faq-item { border-top:1px solid #e6e5db; padding:22px 0; }
.faq-item h3 { font-family:var(--font-display); font-size:18px; font-weight:600; margin-bottom:8px; }
.faq-item p { font-size:16px; line-height:1.65; color:#444; margin:0; }
.post-cta { background:var(--dark); color:var(--off-white); border-radius:20px; padding:44px 40px; margin:56px 0 20px; text-align:center; }
.post-cta p { font-size:19px; line-height:1.6; margin-bottom:24px; }
.post-cta a { display:inline-block; background:var(--teal); color:#08302f; font-weight:700; text-decoration:none; padding:15px 34px; border-radius:50px; font-size:16px; transition:transform .2s ease; }
.post-cta a:hover { transform: translateY(-2px); }
.back-blog { display:inline-block; margin-top:34px; color:var(--red); font-weight:600; text-decoration:none; font-size:15px; }
@media (max-width:640px){ .article{padding:120px 0 30px} .blog-hero{padding:130px 0 55px} .post-grid{padding:50px 0 70px} }
</style>
"""

# ---------- markdown → html ----------
def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    return t

def parse_post(md):
    lines = md.split("\n")
    # título = 1ª linha "# "
    title = ""
    idx = 0
    for i, l in enumerate(lines):
        if l.startswith("# "):
            title = l[2:].strip(); idx = i + 1; break
    rest = lines[idx:]
    # separa CTA (após o último "---")
    cta = ""
    if "---" in rest:
        cut = len(rest) - 1 - rest[::-1].index("---")
        cta_lines = [l for l in rest[cut+1:] if l.strip()]
        cta = " ".join(cta_lines).strip()
        rest = rest[:cut]
    # separa FAQ
    faq = []
    faq_start = None
    for i, l in enumerate(rest):
        if re.match(r'^##\s+Perguntas frequentes', l.strip(), re.I):
            faq_start = i; break
    body_lines = rest if faq_start is None else rest[:faq_start]
    if faq_start is not None:
        q = None; a = []
        for l in rest[faq_start+1:]:
            s = l.strip()
            if not s: continue
            m = re.match(r'^\*\*(.+?)\*\*$', s)
            if m:
                if q: faq.append((q, " ".join(a).strip()))
                q = m.group(1).strip(); a = []
            else:
                a.append(s)
        if q: faq.append((q, " ".join(a).strip()))
    # corpo em blocos
    body_html = []
    quick = None
    para, ul, ol = [], [], []
    def flush():
        nonlocal para, ul, ol
        if para:
            body_html.append("<p>" + inline(" ".join(para).strip()) + "</p>"); para = []
        if ul:
            body_html.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in ul) + "</ul>"); ul = []
        if ol:
            body_html.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in ol) + "</ol>"); ol = []
    for l in body_lines:
        s = l.strip()
        if not s:
            flush(); continue
        if s.startswith("## "):
            flush(); body_html.append(f"<h2>{inline(s[3:].strip())}</h2>"); continue
        if re.match(r'^\*\*Resposta rápida:\*\*', s):
            flush(); quick = inline(s); continue
        mo = re.match(r'^\d+\.\s+(.*)', s)
        if mo:
            if para: flush()
            ol.append(mo.group(1)); continue
        mb = re.match(r'^[-*]\s+(.*)', s)
        if mb:
            if para: flush()
            ul.append(mb.group(1)); continue
        para.append(s)
    flush()
    return {"title": title, "quick": quick, "body": "\n".join(body_html),
            "faq": faq, "cta": cta or "Quer resolver isso do jeito certo? Fale com a Agência MOA."}

# ---------- templates ----------
def page(title, desc, canonical, extra_head, inner):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="article">
<link rel="canonical" href="{canonical}">
<title>{html.escape(title)}</title>
{PRECONNECT}
{FONTS}
{BASE_STYLE}
{BLOG_CSS}
{extra_head}
</head>
<body>
{NAV_ABS}
{inner}
{FOOTER_ABS}
</body>
</html>
"""

def wa_link(msg):
    from urllib.parse import quote
    return f"https://wa.me/{WHATS}?text={quote(msg)}"

def build_article(p, meta):
    title = p["title"]
    slug = meta["slug"]
    canonical = f"{SITE}/blog/{slug}.html"
    date = meta["date"]; read = meta.get("read", 5)
    d = datetime.date.fromisoformat(date)
    date_br = d.strftime("%d/%m/%Y")
    quick = f'<div class="quick-answer">{p["quick"]}</div>' if p["quick"] else ""
    faq_html = ""
    if p["faq"]:
        items = "".join(f'<div class="faq-item"><h3>{inline(q)}</h3><p>{inline(a)}</p></div>' for q, a in p["faq"])
        faq_html = f'<h2>Perguntas frequentes</h2><div class="faq">{items}</div>'
    cta_html = (f'<div class="post-cta"><p>{inline(p["cta"])}</p>'
                f'<a href="{wa_link("Oi! Vim pelo blog da MOA e quero falar sobre meu negócio.")}" '
                f'target="_blank" rel="noopener">Falar com a MOA no WhatsApp</a></div>')
    # JSON-LD
    ld = [
        {"@context":"https://schema.org","@type":"Article","headline":title,
         "description":meta["description"],"datePublished":f"{date}T09:00:00-03:00",
         "dateModified":f"{date}T09:00:00-03:00","inLanguage":"pt-BR",
         "author":{"@type":"Organization","name":"Agência MOA","url":SITE},
         "publisher":{"@type":"Organization","name":"Agência MOA","url":SITE},
         "mainEntityOfPage":{"@type":"WebPage","@id":canonical}},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"Início","item":SITE+"/"},
            {"@type":"ListItem","position":2,"name":"Blog","item":SITE+"/blog/"},
            {"@type":"ListItem","position":3,"name":title,"item":canonical}]},
    ]
    if p["faq"]:
        ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in p["faq"]]})
    ld_html = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    inner = f"""
<article class="article">
  <div class="container"><div class="article-wrap">
    <nav class="breadcrumb"><a href="/">Início</a> / <a href="/blog/">Blog</a> / {html.escape(title)}</nav>
    <span class="article-cat">{html.escape(meta["category"])}</span>
    <h1>{html.escape(title)}</h1>
    <div class="article-meta">{date_br} · {read} min de leitura</div>
    {quick}
    <div class="article-body">
      {p["body"]}
      {faq_html}
    </div>
    {cta_html}
    <a class="back-blog" href="/blog/">← Voltar para o blog</a>
  </div></div>
</article>
"""
    return page(f"{title} | Blog Agência MOA", meta["description"], canonical, ld_html, inner)

def build_index(items):
    canonical = f"{SITE}/blog/"
    cards = ""
    for p, meta in items:
        d = datetime.date.fromisoformat(meta["date"]).strftime("%d/%m/%Y")
        cards += f"""<a class="post-card" href="/blog/{meta['slug']}.html">
  <span class="post-cat">{html.escape(meta['category'])}</span>
  <h2>{html.escape(p['title'])}</h2>
  <p>{html.escape(meta['description'])}</p>
  <div class="post-meta">{d} · {meta.get('read',5)} min</div>
  <div class="post-more">Ler artigo →</div>
</a>
"""
    ld = {"@context":"https://schema.org","@type":"Blog","name":"Blog da Agência MOA",
          "url":canonical,"description":BLOG_DESC,
          "publisher":{"@type":"Organization","name":"Agência MOA","url":SITE}}
    ld_html = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    inner = f"""
<header class="blog-hero"><div class="container">
  <span class="label">Blog</span>
  <h1>Ideias que fazem seu negócio ser encontrado</h1>
  <p>{BLOG_DESC}</p>
</div></header>
<section><div class="container"><div class="post-grid">
{cards}</div></div></section>
"""
    return page("Blog | Agência MOA — Marketing, Google e Tráfego", BLOG_DESC, canonical, ld_html, inner)

# ---------- run ----------
def main():
    with open(os.path.join(HERE, "posts.json"), encoding="utf-8") as f:
        manifest = json.load(f)["posts"]
    built = []
    for meta in manifest:
        with open(os.path.join(HERE, "_posts", meta["slug"] + ".md"), encoding="utf-8") as f:
            p = parse_post(f.read())
        out = os.path.join(HERE, meta["slug"] + ".html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(build_article(p, meta))
        built.append((p, meta))
        print("artigo:", meta["slug"] + ".html")
    # listagem (mais novo primeiro)
    order = sorted(built, key=lambda x: x[1]["date"], reverse=True)
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_index(order))
    print("listagem: blog/index.html")
    update_sitemap(manifest)
    update_llms(manifest)

def update_sitemap(manifest):
    path = os.path.join(ROOT, "sitemap.xml")
    with open(path, encoding="utf-8") as f:
        xml = f.read()
    today = datetime.date.today().isoformat()
    urls = [(f"{SITE}/blog/", "0.7")] + [(f"{SITE}/blog/{m['slug']}.html", "0.6") for m in manifest]
    block = ""
    for loc, pri in urls:
        if loc in xml:
            continue
        block += (f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n"
                  f"    <changefreq>monthly</changefreq>\n    <priority>{pri}</priority>\n  </url>\n")
    if block:
        xml = xml.replace("</urlset>", block + "</urlset>")
        with open(path, "w", encoding="utf-8") as f:
            f.write(xml)
        print("sitemap.xml atualizado (+%d urls)" % block.count("<url>"))
    else:
        print("sitemap.xml já continha as urls do blog")

def update_llms(manifest):
    path = os.path.join(ROOT, "llms.txt")
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    if "## Blog" in txt:
        print("llms.txt já tinha seção Blog"); return
    lines = ["\n## Blog",
             f"\nArtigos práticos da MOA sobre Google, tráfego pago e presença digital para pequenas empresas. Listagem em {SITE}/blog/.\n"]
    for m in manifest:
        lines.append(f"- [{m['slug'].replace('-', ' ')}]({SITE}/blog/{m['slug']}.html): {m['description']}")
    # insere antes de "## Contato" se existir, senão no fim
    add = "\n".join(lines) + "\n"
    if "## Contato" in txt:
        txt = txt.replace("## Contato", add + "\n## Contato", 1)
    else:
        txt = txt.rstrip() + "\n" + add
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("llms.txt atualizado (seção Blog)")

if __name__ == "__main__":
    main()
