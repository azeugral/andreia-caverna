"""Monta as páginas da raiz a partir de tools/paginas/*.html (logo centralizado, barra de menu e rodapé comuns).
Troque V para furar o cache de CSS/JS.
Marcadores nas páginas: <!--seta-->, <!--brilho--> e <!--zap-->."""
import os, re, glob
V = '1'
AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
BASE = 'https://azeugral.github.io/andreia-caverna/'  # CONFIRMAR: trocar quando houver domínio
ZAP = 'https://wa.me/5511972260964'  # CONFIRMAR o DDD: o post mostra só 97226-0964

SETA = '<svg class="i-seta" viewBox="0 0 18 18" aria-hidden="true"><path d="M2 9h13M10 4l5 5-5 5"/></svg>'
# o brilho de 4 pontas que aparece ao lado do C no logo dela
BRILHO = '<svg class="i-brilho" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0c.7 6.6 4.4 10.6 12 12-7.6 1.4-11.3 5.4-12 12-.7-6.6-4.4-10.6-12-12C7.6 10.6 11.3 6.6 12 0z"/></svg>'

HEAD = '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#0d0c0b">
<meta property="og:type" content="website">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{base}og-caverna.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Logo Caverna Hair e Makeup, em dourado sobre preto">
<meta property="og:locale" content="pt_BR">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" href="favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/img/icone-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/css/site.css?v={v}">
</head>
<body class="{corpo}">
<a class="sr" href="#conteudo">Pular para o conteúdo</a>
<div class="progresso" data-prog aria-hidden="true"><i></i></div>
<header class="topo">
  <a class="topo-logo" href="./" aria-label="Caverna Hair e Makeup, início"><img src="assets/img/logo-caverna-360.webp" srcset="assets/img/logo-caverna-360.webp 360w, assets/img/logo-caverna-720.webp 720w" sizes="(min-width:900px) 300px, 220px" alt="Caverna Hair e Makeup" width="720" height="417"></a>
</header>
<nav class="barra" aria-label="Principal">
  <a class="barra-marca" href="./" aria-label="Caverna Hair e Makeup, início"><img src="assets/img/logo-caverna-360.webp" alt="" width="360" height="208"></a>
  <button class="barra-abrir" type="button" aria-expanded="false" aria-controls="menu"><span>Menu</span><i aria-hidden="true"></i></button>
  <ul class="menu" id="menu">{menu}</ul>
  <a class="btn peq barra-cta" href="agendar.html"><span>Agendar</span><i>{brilho}</i></a>
</nav>
<main id="conteudo">
'''

FOOT = '''</main>
<footer class="rodape">
  <div class="wrap">
    <a class="rodape-logo" href="./" aria-label="Caverna Hair e Makeup, início"><img src="assets/img/logo-caverna-360.webp" srcset="assets/img/logo-caverna-360.webp 360w, assets/img/logo-caverna-720.webp 720w" sizes="260px" alt="Caverna Hair e Makeup" width="720" height="417" loading="lazy"></a>
    <p class="rodape-frase">Andréia Oliveira · cabeleireira e maquiadora</p>
    <div class="colunas">
      <div><h4>Páginas</h4><ul><li><a href="./">Início</a></li><li><a href="./#servicos">Serviços</a></li><li><a href="trabalhos.html">Trabalhos</a></li><li><a href="agendar.html">Agendar</a></li></ul></div>
      <div><h4>Contato</h4><ul><li><a href="{zap}" target="_blank" rel="noopener">WhatsApp 97226-0964</a></li><li><a href="https://www.instagram.com/andreiacaverna_hairemakeup/" target="_blank" rel="noopener">Instagram @andreiacaverna_hairemakeup</a></li></ul></div>
      <div><h4>Atendimento</h4><ul><li>São Paulo, SP</li><li>Estúdio: <em class="a-preencher">bairro a preencher</em></li><li>Em domicílio, com hora marcada</li></ul></div>
    </div>
    <div class="base"><span>© <span data-ano>2026</span> Caverna Hair e Makeup. Todos os direitos reservados.</span><span>Site por <a href="https://lrgz.com.br" target="_blank" rel="noopener">L R G Z</a></span></div>
  </div>
</footer>
<a class="fixo" href="agendar.html" aria-label="Agendar horário">{brilho}<span>Agendar</span></a>
{extra}<script src="assets/js/obras.js?v={v}"></script>
<script src="assets/js/site.js?v={v}"></script>
</body>
</html>
'''

LB = '''<div class="lb" role="dialog" aria-modal="true" aria-label="Foto ampliada" aria-hidden="true">
  <div class="lb-topo"><span class="rot" data-cont></span><button type="button" data-fechar>Fechar</button></div>
  <div class="lb-palco"><img alt=""></div>
  <div class="lb-base"><button type="button" data-ant aria-label="Anterior">&larr;</button><span class="rot" data-leg></span><button type="button" data-prox aria-label="Próxima">&rarr;</button></div>
</div>
'''

MENU = [('./', 'Início'), ('./#servicos', 'Serviços'), ('trabalhos.html', 'Trabalhos'), ('./#noivas', 'Noivas'), ('./#sobre', 'Sobre')]
ATUAL = ' aria-current="page"'

for f in glob.glob(os.path.join(AQUI, 'paginas', '*.html')):
    nome = os.path.basename(f)
    txt = open(f, encoding='utf-8').read()
    meta = dict(re.findall(r'<!--\s*(\w+):\s*(.*?)\s*-->', txt.split('\n---\n')[0]))
    corpo = txt.split('\n---\n', 1)[1].replace('<!--seta-->', SETA).replace('<!--brilho-->', BRILHO).replace('<!--zap-->', ZAP)
    atual = {'index.html': './', '404.html': None}.get(nome, nome)
    menu = ''.join(f'<li><a href="{h}"' + (ATUAL if h == atual else '') + f'>{t}</a></li>' for h, t in MENU)
    html = HEAD.format(titulo=meta['titulo'], desc=meta['desc'], base=BASE, v=V, menu=menu, brilho=BRILHO,
                       corpo='inicio' if nome == 'index.html' else 'interna') + corpo + \
        FOOT.format(v=V, zap=ZAP, brilho=BRILHO, extra=LB if meta.get('lightbox') == 'sim' else '')
    if nome == '404.html':
        html = html.replace('<head>', '<head>\n<base href="/andreia-caverna/">', 1)
    if nome == 'agendar.html':
        html = html.replace('<a class="fixo"', '<a hidden class="fixo"', 1)
    open(os.path.join(SITE, nome), 'w', encoding='utf-8', newline='\n').write(html)
    print('ok', nome)
