#!/usr/bin/env python3
"""
Gera as páginas de nicho da MOA reusando o casco do index.html.
Casco = head + nav (até <!-- HERO -->) e rodapé + scripts (de <!-- FOOTER -->).
Corta por MARCADOR, nunca por número de linha (o index muda de tamanho).
Miolo é próprio de cada nicho (não é clone da home -> evita página-porta).
Rodar de dentro de ~/Documents/Criador de Sites/agencia-moa
"""
import json, pathlib, sys

BASE = pathlib.Path.home() / "Documents/Criador de Sites/agencia-moa"
SITE = "https://agenciamoa.com.br"
TEL = "+5588988575422"
ARROW = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>')
ARROW_BIG = ARROW.replace('width="16" height="16"', 'width="18" height="18"')

FAQ_CSS = '''
/* FAQ — páginas de nicho */
.faq-sec { padding: 120px 0; background: var(--off-white); }
.faq-list { max-width: 820px; margin: 48px auto 0; }
.faq-item { border-bottom: 1px solid rgba(27,27,27,.12); }
.faq-item summary { font-family: var(--font-display); font-weight: 600; font-size: 20px;
  padding: 26px 0; cursor: pointer; list-style: none; display: flex; justify-content: space-between;
  align-items: center; gap: 24px; transition: color .2s; }
.faq-item summary::-webkit-details-marker { display: none; }
.faq-item summary:hover { color: var(--orange); }
.faq-item summary::after { content: "+"; color: var(--orange); font-size: 28px; font-weight: 300; flex-shrink: 0; }
.faq-item[open] summary::after { content: "–"; }
.faq-item p { padding-bottom: 26px; color: rgba(27,27,27,.72); font-size: 16.5px; line-height: 1.75; max-width: 90%; }
@media (max-width: 700px) { .faq-sec { padding: 80px 0; } .faq-item summary { font-size: 17px; } }
'''

# ------------------------------------------------------------------ NICHOS
NICHOS = [
 {
  "slug": "marketing-para-medicos-em-teresina",
  "title": "Marketing para Médicos em Teresina | Agência MOA",
  "desc": ("Marketing médico em Teresina-PI dentro das regras do CFM: Google Meu Negócio, "
           "tráfego pago e presença digital para consultórios e clínicas. Fale com a MOA."),
  "eyebrow": "marketing médico · Teresina-PI",
  "h1": 'Marketing para<br>\n      <span>médicos</span> em<br>\n      Teresina.',
  "sub": ("Seu paciente procura no Google antes de escolher. A MOA cuida da sua presença digital "
          "para que ele encontre você — com estratégia e dentro das regras do CFM."),
  "wa": "Ol%C3%A1!%20Sou%20m%C3%A9dico%20e%20quero%20saber%20do%20marketing%20para%20consult%C3%B3rio.",
  "service_type": "Marketing para médicos e clínicas",
  "service_name": "Marketing médico em Teresina",
  "service_desc": ("Presença digital, Google Meu Negócio e tráfego pago para consultórios e clínicas "
                   "em Teresina-PI, dentro das regras de publicidade médica do CFM."),
  "audience": "Médicos, consultórios e clínicas",
  "problem_h2": 'Ser um bom médico não basta se ninguém te acha.',
  "problem_ps": [
    "Hoje, quem procura um médico em Teresina digita a especialidade no Google ou abre o Maps. Escolhe entre os primeiros perfis que aparecem, olha as avaliações e chama no WhatsApp. Se o seu consultório não está lá, ele nem chega a considerar você — por melhor que seja o seu trabalho.",
    "O outro lado é que marketing médico tem regra. O CFM limita como o médico pode se comunicar, e muito consultório trava por medo de errar — ou pior, contrata uma agência que não conhece essas regras e expõe o profissional.",
    "A MOA resolve os dois lados: coloca você onde o paciente procura, sem sair do que o CFM permite.",
  ],
  "pills": [("dark","Google Meu Negócio"),("orange","Tráfego pago"),("teal","Site do consultório"),("red","Dentro do CFM")],
  "services_h2": 'Do primeiro clique ao <span>agendamento.</span>',
  "services_label": "o que fazemos pelo seu consultório",
  "services": [
    ("Google Meu Negócio","É o que mais traz paciente no começo. Perfil completo, especialidade certa, fotos reais do consultório e estratégia para colher avaliações.",["Perfil e categoria","Fotos","Avaliações","Maps"]),
    ("Tráfego pago para saúde","Campanhas no Google e Meta que colocam seu consultório na frente de quem já procura sua especialidade em Teresina — sem desperdiçar verba.",["Google Ads","Meta Ads","Conversão WhatsApp","Relatórios"]),
    ("Página do consultório","Um site rápido e claro: sua especialidade, sua formação, onde fica e um caminho fácil até o WhatsApp. Feito para virar agendamento.",["Landing page","Mobile","SEO local","WhatsApp"]),
    ("Fotografia do consultório","Imagem profissional do espaço e do profissional. Paciente confia no que vê — e foto de banco de imagem não constrói confiança.",["Retrato","Ambiente","Equipe"]),
    ("Conteúdo dentro do CFM","Presença nas redes com informação de valor e linguagem correta: sem promessa de resultado, sem sensacionalismo, sem expor você.",["Instagram","Educação","Conformidade"]),
    ("Acompanhamento","Você enxerga quantos contatos chegaram e de onde vieram. Sem relatório enfeitado — número real, decisão baseada em dado.",["Métricas","Origem do lead","Ajuste contínuo"]),
  ],
  "faq_h2": 'Dúvidas de quem tem <span>consultório.</span>',
  "faq": [
    ("Médico pode fazer anúncio e marketing no Brasil?",
     "Pode. A publicidade médica é permitida, mas segue regras do Conselho Federal de Medicina (CFM). Na prática: sem promessa ou garantia de resultado, sem sensacionalismo, sem usar o antes e depois como apelo comercial, sem concorrer preço ou promoção, e sempre identificando o profissional com nome e CRM. A MOA trabalha dentro dessas regras desde o planejamento da campanha."),
    ("O que mais traz paciente para um consultório em Teresina?",
     "Na maioria dos casos, o Google Meu Negócio bem configurado é o que traz mais retorno no começo — quem procura um médico na cidade busca no Google ou no Maps e escolhe entre os primeiros perfis, olhando avaliações. Depois disso, tráfego pago no Google Ads e uma página de consultório que explique a especialidade e facilite o contato."),
    ("Preciso ter site para divulgar meu consultório?",
     "Não é obrigatório para começar, mas ajuda bastante. O Google Meu Negócio já resolve a busca local. O site (ou uma página de consultório) entra para dar credibilidade, explicar a especialidade, receber campanhas de anúncio e transformar visitante em agendamento pelo WhatsApp."),
    ("Quanto tempo leva para o consultório aparecer no Google?",
     "O perfil no Google Meu Negócio costuma aparecer nas buscas locais em poucos dias após a verificação. Ganhar posição entre os primeiros depende de constância: perfil completo, avaliações de pacientes e informação atualizada. Já as campanhas de tráfego pago colocam o consultório na frente do paciente desde o primeiro dia."),
  ],
  "cta_h2": 'Seu paciente está <span>procurando.</span>',
  "cta_p": "Uma conversa de diagnóstico, sem compromisso, para entender onde seu consultório está perdendo paciente — e o que dá para resolver primeiro.",
 },
 {
  "slug": "marketing-para-restaurantes-em-teresina",
  "title": "Marketing para Restaurantes em Teresina | Agência MOA",
  "desc": ("Marketing para restaurantes, bares e cafés em Teresina-PI: Google Meu Negócio, "
           "fotografia gastronômica, redes sociais e tráfego pago. Fale com a MOA."),
  "eyebrow": "marketing gastronômico · Teresina-PI",
  "h1": 'Marketing para<br>\n      <span>restaurantes</span><br>\n      em Teresina.',
  "sub": ("Seu cliente escolhe onde comer olhando foto e avaliação no celular — antes de sair de casa. "
          "A MOA cuida pra que essa escolha seja o seu restaurante."),
  "wa": "Ol%C3%A1!%20Tenho%20um%20restaurante%20e%20quero%20saber%20do%20marketing%20com%20a%20MOA.",
  "service_type": "Marketing para restaurantes, bares e cafés",
  "service_name": "Marketing para restaurantes em Teresina",
  "service_desc": ("Google Meu Negócio, fotografia gastronômica, redes sociais e tráfego pago para "
                   "restaurantes, bares, cafés e cervejarias em Teresina-PI."),
  "audience": "Restaurantes, bares, cafés e cervejarias",
  "problem_h2": 'A comida é ótima. Mas a decisão acontece antes do prato.',
  "problem_ps": [
    "Ninguém mais sai de casa sem pesquisar. A pessoa abre o Google ou o Maps, procura onde comer perto dali, olha a nota, as fotos e as avaliações — e decide em segundos. Se o seu restaurante aparece com foto escura, informação desatualizada ou sem avaliação recente, ele é descartado antes de ter chance.",
    "O outro lado é a dependência: muito restaurante em Teresina vive refém do iFood e do alcance do Instagram. Quando a taxa sobe ou o algoritmo muda, o movimento cai — e não há canal próprio para segurar.",
    "A MOA trabalha os dois: faz seu restaurante ser escolhido na hora da decisão e constrói canais que são seus.",
  ],
  "pills": [("dark","Google Meu Negócio"),("orange","Fotografia gastronômica"),("teal","Redes e conteúdo"),("red","Tráfego local")],
  "services_h2": 'Da vitrine digital à <span>mesa cheia.</span>',
  "services_label": "o que fazemos pelo seu restaurante",
  "services": [
    ("Google Meu Negócio","É onde a decisão acontece. Perfil completo, categoria certa, horário sempre atualizado, cardápio, fotos que abrem apetite e rotina para colher avaliações.",["Perfil e Maps","Avaliações","Cardápio","Fotos"]),
    ("Fotografia gastronômica","O prato precisa vender sozinho. Fotografia profissional de comida, bebida e ambiente — o serviço que a MOA já faz para o setor há anos.",["Prato","Ambiente","Bebida","Cardápio"]),
    ("Redes sociais","Instagram é a vitrine do restaurante. Conteúdo com constância e identidade, feito para dar fome — não para preencher grade.",["Instagram","Reels","Conteúdo","Planejamento"]),
    ("Tráfego pago local","Restaurante é negócio de raio. Campanhas segmentadas por região, horário e ocasião — almoço, happy hour, fim de semana — sem queimar verba com quem não vem.",["Meta Ads","Google Ads","Geolocalização","Sazonalidade"]),
    ("Vídeo e ambiente","Vídeo mostra o que a foto não conta: o movimento, o som, a brasa, o corte. Produção audiovisual para redes e anúncios.",["Reels","Institucional","Making of"]),
    ("Canal próprio","Site com cardápio digital, reserva ou pedido direto. Menos dependência de aplicativo e de taxa — um canal que é seu.",["Cardápio digital","Pedido direto","SEO local","WhatsApp"]),
  ],
  "faq_h2": 'Dúvidas de quem tem <span>restaurante.</span>',
  "faq": [
    ("O que mais traz cliente para um restaurante em Teresina?",
     "Na maioria dos casos, o Google Meu Negócio somado às avaliações. Quem procura onde comer abre o Google ou o Maps, filtra por perto, olha a nota e as fotos, e decide ali. Um perfil completo, com fotos boas do prato e do ambiente e uma rotina de avaliações, costuma render mais que qualquer anúncio isolado. Depois entram Instagram e tráfego pago geolocalizado."),
    ("Foto de comida faz diferença de verdade?",
     "Faz — e costuma ser o fator mais subestimado. A decisão de onde comer é visual: a pessoa escolhe o prato antes de escolher o restaurante. Foto escura ou tirada no improviso derruba a percepção de valor e o preço que o cliente aceita pagar. Fotografia gastronômica é um dos serviços que a MOA já faz para o setor."),
    ("Preciso de site se já tenho Instagram e iFood?",
     "Para começar, não. O Google Meu Negócio e o Instagram já resolvem a descoberta. O site (ou uma página com cardápio digital) entra quando você quer reduzir a dependência do iFood e das taxas, receber reserva ou pedido direto, e ter um canal que é seu — que não depende do algoritmo nem da política de um aplicativo."),
    ("Vale a pena anunciar no Instagram para restaurante?",
     "Vale, desde que seja geolocalizado e o criativo seja bom. Restaurante é negócio de bairro e de raio: não adianta alcançar a cidade inteira se a pessoa não vai atravessar Teresina para almoçar. Trabalhamos campanhas segmentadas por região, horário e ocasião de consumo, medindo o que vira cliente na porta."),
  ],
  "cta_h2": 'Sua próxima mesa cheia <span>começa aqui.</span>',
  "cta_p": "Uma conversa de diagnóstico, sem compromisso, para entender onde seu restaurante está perdendo cliente — e o que dá para resolver primeiro.",
 },
 {
  "slug": "marketing-para-hoteis-em-teresina",
  "title": "Marketing para Hotéis e Pousadas em Teresina | Agência MOA",
  "desc": ("Marketing para hotéis e pousadas em Teresina-PI: Google Meu Negócio, fotografia de "
           "hospedagem, reserva direta e tráfego pago. Menos dependência de OTA. Fale com a MOA."),
  "eyebrow": "marketing para hotelaria · Teresina-PI",
  "h1": 'Marketing para<br>\n      <span>hotéis</span> em<br>\n      Teresina.',
  "sub": ("O hóspede compara foto, nota e preço antes de reservar — e boa parte dessa reserva vai "
          "embora em comissão. A MOA trabalha sua ocupação e o seu canal direto."),
  "wa": "Ol%C3%A1!%20Tenho%20um%20hotel%20e%20quero%20saber%20do%20marketing%20com%20a%20MOA.",
  "service_type": "Marketing para hotéis, pousadas e hospedagem",
  "service_name": "Marketing para hotelaria em Teresina",
  "service_desc": ("Google Meu Negócio, fotografia de hospedagem, reserva direta e tráfego pago para "
                   "hotéis e pousadas em Teresina-PI, com foco em ocupação e menos dependência de OTAs."),
  "audience": "Hotéis, pousadas e meios de hospedagem",
  "problem_h2": 'Você paga comissão por um hóspede que já era seu.',
  "problem_ps": [
    "Teresina recebe gente o ano inteiro por trabalho, eventos e tratamento de saúde. Só que a maior parte dessa procura passa por uma OTA — Booking, Airbnb, Decolar. O hóspede acha lá, reserva lá, e uma fatia da diária vai embora em comissão. Muitas vezes ele já teria escolhido você de qualquer jeito.",
    "Existe um comportamento conhecido: a pessoa descobre o hotel na OTA, mas antes de fechar procura o nome dele no Google para ver as fotos, as avaliações e o site. Se nesse momento ela não encontra um perfil bem cuidado e um caminho fácil de reservar direto, ela volta pra OTA — e você paga a comissão.",
    "A MOA cuida exatamente desse momento: ser encontrado, gerar confiança e ter um canal direto pronto para receber a reserva.",
  ],
  "pills": [("dark","Google Meu Negócio"),("orange","Fotografia de hospedagem"),("teal","Reserva direta"),("red","Tráfego pago")],
  "services_h2": 'Da busca à <span>reserva direta.</span>',
  "services_label": "o que fazemos pelo seu hotel",
  "services": [
    ("Google Meu Negócio","O perfil que aparece quando procuram hotel em Teresina — ou procuram o seu nome antes de fechar. Fotos, comodidades, localização e rotina de avaliações.",["Perfil e Maps","Avaliações","Fotos","Comodidades"]),
    ("Fotografia de hospedagem","Quarto, área comum, café da manhã, fachada. O hóspede compra o que vê — e foto fraca derruba a diária que você consegue cobrar.",["Quartos","Áreas comuns","Gastronomia","Fachada"]),
    ("Reserva direta","Site e página de reservas que tiram o intermediário do caminho: menos comissão por hóspede e um canal que é seu.",["Site","Motor de reserva","WhatsApp","SEO local"]),
    ("Tráfego pago","Campanhas para quem já procura hospedagem em Teresina, e para as demandas que a cidade tem o ano todo: corporativo, eventos e acompanhantes de tratamento.",["Google Ads","Meta Ads","Segmentação","Sazonalidade"]),
    ("Vídeo e tour","Vídeo do quarto e das áreas comuns responde a dúvida que trava a reserva — e funciona em anúncio, site e redes.",["Tour","Reels","Institucional"]),
    ("Reputação","Avaliação é moeda em hotelaria. Estratégia para colher avaliações boas com constância e cuidar do que já está publicado.",["Google","Reviews","Constância"]),
  ],
  "faq_h2": 'Dúvidas de quem tem <span>hotel.</span>',
  "faq": [
    ("Como reduzir a dependência de Booking e outras OTAs?",
     "Não é deixar a OTA — é deixar de pagar comissão por quem já ia escolher você. O caminho: um perfil forte no Google Meu Negócio e um canal de reserva direta fácil de achar. Muita gente descobre o hotel na OTA, mas pesquisa o nome dele no Google antes de fechar. Se nesse momento existe um site bom com reserva direta, essa reserva entra sem comissão."),
    ("O que mais traz hóspede para um hotel em Teresina?",
     "Além das OTAs, o Google Meu Negócio e as avaliações. Quem chega a Teresina por trabalho, evento ou tratamento de saúde costuma buscar hospedagem no Google ou no Maps, olhando localização, nota e fotos. Um perfil completo e bem avaliado aparece nessa hora. Depois entram tráfego pago e o canal de reserva direta."),
    ("Foto de quarto faz diferença na diária?",
     "Faz. Hospedagem é compra visual e feita à distância: o hóspede decide sem ver o lugar. Foto profissional de quarto, área comum e café da manhã eleva a percepção de valor e sustenta uma diária maior — enquanto foto escura ou tirada de celular empurra a escolha para o preço."),
    ("Vale a pena ter site próprio se já estou nas OTAs?",
     "Vale, e costuma se pagar rápido. Cada reserva direta é uma diária cheia, sem comissão. O site também é onde o hóspede confere se o hotel é o que a OTA prometeu — ele fecha ali ou desiste. É o canal que não depende da política nem do algoritmo de um aplicativo."),
  ],
  "cta_h2": 'Mais ocupação, <span>menos comissão.</span>',
  "cta_p": "Uma conversa de diagnóstico, sem compromisso, para entender onde seu hotel está deixando reserva (e margem) na mesa.",
 },
]

# ------------------------------------------------------------------ BUILD
def build(src, n):
    url = f"{SITE}/{n['slug']}.html"
    wa = f"https://wa.me/5588988575422?text={n['wa']}"

    for m in ["<!-- HERO -->", "<!-- FOOTER -->", "<!-- CLIENTS -->", "<!-- TEAM -->"]:
        if m not in src:
            sys.exit(f"ERRO: marcador {m} não encontrado no index.html")

    top = src.split("<!-- HERO -->")[0]
    bottom = "<!-- FOOTER -->" + src.split("<!-- FOOTER -->", 1)[1]
    # prova social: mesma vitrine de clientes da home (sem rótulo de segmento)
    clients = "<!-- CLIENTS -->" + src.split("<!-- CLIENTS -->", 1)[1].split("<!-- TEAM -->")[0]
    clients = clients.replace('<section class="clients" id="clients">', '<section class="clients">')

    # ---- head/SEO
    reps = [
     ('<meta name="description" content="Agência MOA em Teresina-PI — estratégia, design, marketing digital e produção audiovisual. Transformamos sua ideia em presença real. Do conceito à entrega, sem atalhos.">',
      f'<meta name="description" content="{n["desc"]}">'),
     ('<meta property="og:title" content="Agência MOA — Marketing Digital e Design em Teresina-PI">',
      f'<meta property="og:title" content="{n["title"]}">'),
     ('<meta property="og:description" content="Estratégia, design, marketing digital e produção audiovisual em Teresina-PI. Do conceito à entrega, sem atalhos.">',
      f'<meta property="og:description" content="{n["desc"]}">'),
     ('<title>Agência MOA — Marketing Digital e Design em Teresina-PI</title>', f'<title>{n["title"]}</title>'),
     ('<meta property="og:url" content="https://agenciamoa.com.br/">', f'<meta property="og:url" content="{url}">'),
     ('<link rel="canonical" href="https://agenciamoa.com.br/">', f'<link rel="canonical" href="{url}">'),
    ]
    for a, b in reps:
        if a not in top:
            sys.exit(f"ERRO [{n['slug']}]: trecho de head não encontrado -> {a[:60]}")
        top = top.replace(a, b)

    # ---- schema Service + FAQPage
    service = {"@context":"https://schema.org","@type":"Service","serviceType":n["service_type"],
      "name":n["service_name"],"description":n["service_desc"],"url":url,
      "provider":{"@type":"MarketingAgency","name":"Agência MOA","url":SITE,"telephone":TEL},
      "areaServed":{"@type":"City","name":"Teresina"},
      "audience":{"@type":"Audience","audienceType":n["audience"]}}
    faqpage = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
      {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in n["faq"]]}
    schema = ('<script type="application/ld+json">\n' + json.dumps(service, ensure_ascii=False, indent=2) +
              '\n</script>\n<script type="application/ld+json">\n' +
              json.dumps(faqpage, ensure_ascii=False, indent=2) + '\n</script>\n')
    top = top.replace('<script defer src="https://analytics.agenciamoa.com.br/script.js"',
                      schema + '<script defer src="https://analytics.agenciamoa.com.br/script.js"')
    top = top.replace('</style>', FAQ_CSS + '</style>', 1)

    # ---- âncoras: seções que não existem aqui apontam pra home
    for a in ["manifesto", "services", "clients", "team", "labs"]:
        top = top.replace(f'href="#{a}"', f'href="index.html#{a}"')
        bottom = bottom.replace(f'href="#{a}"', f'href="index.html#{a}"')

    cards = "\n".join(
      f'''      <div class="service-card reveal">
        <span class="service-number">{i:02d}</span>
        <h3>{t}</h3>
        <p>{d}</p>
        <div class="service-tags">
{chr(10).join(f'          <span class="service-tag">{tag}</span>' for tag in tags)}
        </div>
      </div>''' for i, (t, d, tags) in enumerate(n["services"], 1))

    pills = "\n".join(f'          <span class="pill pill-{c}">{t}</span>' for c, t in n["pills"])
    probs = "\n".join(f'        <p>{p}</p>' for p in n["problem_ps"])
    faqs = "\n".join(
      f'''      <details class="faq-item"{" open" if i == 0 else ""}>
        <summary>{q}</summary>
        <p>{a}</p>
      </details>''' for i, (q, a) in enumerate(n["faq"]))

    body = f'''<!-- HERO -->
<section class="hero">
  <div class="hero-content">
    <p class="hero-eyebrow">{n["eyebrow"]}</p>
    <h1 class="hero-title">
      {n["h1"]}
    </h1>
    <p class="hero-sub">
      {n["sub"]}
    </p>
    <div class="hero-actions">
      <a href="{wa}" class="btn btn-primary">
        Falar com a MOA
        {ARROW}
      </a>
      <a href="#como-funciona" class="btn btn-outline">Como funciona</a>
    </div>
  </div>
  <div class="hero-stripes-wrap">
    <div class="hstripe hstripe-1"></div>
    <div class="hstripe hstripe-2"></div>
    <div class="hstripe hstripe-3"></div>
    <div class="hstripe hstripe-4"></div>
    <div class="hstripe hstripe-5"></div>
  </div>
</section>

<!-- CONTEXTO -->
<section class="manifesto" id="como-funciona">
  <div class="container">
    <div class="manifesto-inner">
      <div class="manifesto-text reveal">
        <span class="label">o problema</span>
        <h2><span class="reveal-text"><span class="reveal-text-inner">{n["problem_h2"]}</span></span></h2>
{probs}
        <div class="manifesto-pills">
{pills}
        </div>
      </div>
      <div class="manifesto-visual reveal">
        <img src="assets/img/hero-manifesto.webp" alt="Equipe da agência MOA em Teresina" class="manifesto-img" loading="lazy" style="border-radius:4px; object-fit:cover; aspect-ratio:1/1;">
      </div>
    </div>
  </div>
</section>

<!-- SERVIÇOS -->
<section class="services">
  <div class="container">
    <div class="services-header reveal">
      <span class="label label--light">{n["services_label"]}</span>
      <h2><span class="reveal-text"><span class="reveal-text-inner">{n["services_h2"]}</span></span></h2>
    </div>
    <div class="services-grid">
{cards}
    </div>
  </div>
</section>

{clients}
<!-- FAQ -->
<section class="faq-sec">
  <div class="container">
    <div class="services-header reveal" style="text-align:center;">
      <span class="label">perguntas frequentes</span>
      <h2><span class="reveal-text"><span class="reveal-text-inner">{n["faq_h2"]}</span></span></h2>
    </div>
    <div class="faq-list">
{faqs}
    </div>
  </div>
</section>

<!-- CTA FINAL -->
<section class="cta-final" id="contact">
  <div class="container">
    <div class="cta-final-inner">
      <span class="label label--light">vamos conversar</span>
      <h2><span class="reveal-text"><span class="reveal-text-inner">{n["cta_h2"]}</span></span></h2>
      <p>{n["cta_p"]}</p>
      <a href="{wa}" class="btn btn-primary" style="margin: 0 auto; font-size: 15px; padding: 18px 44px;">
        Fala com a MOA no WhatsApp
        {ARROW_BIG}
      </a>
    </div>
  </div>
</section>

'''
    (BASE / f"{n['slug']}.html").write_text(top + body + bottom, encoding="utf-8")
    return n["slug"]


if __name__ == "__main__":
    src = (BASE / "index.html").read_text(encoding="utf-8")
    for n in NICHOS:
        print("OK ->", build(src, n) + ".html")
