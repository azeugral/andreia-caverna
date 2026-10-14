"""Gera assets/obras/*.webp, assets/js/obras.js, o logo Caverna, as fotos da Andréia, favicons e og-caverna.jpg.

Originais em ../_ref/ig (extraídos do Instagram @andreiacaverna_hairemakeup em 13/10/2026).
Os números são os da folha de contato ../_ref/contato/*.jpg e da lista ../_ref/legendas.txt
(000 = post mais recente). As legendas abaixo resumem o que ela mesma escreveu no post.
"""
import glob, json, os
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter, ImageChops

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
REF = os.path.join(SITE, '..', '_ref')
IG = os.path.join(REF, 'ig')
OUT = os.path.join(SITE, 'assets', 'obras')
IMG = os.path.join(SITE, 'assets', 'img')

MARFIM = (250, 246, 240)
NUDE = (238, 223, 213)
CHAMPANHE = (140, 106, 66)   # #8c6a42, o dourado do logo escurecido para fundo claro
CACAU = (43, 33, 29)

C, M, P = 'cabelo', 'make', 'penteado'
OBRAS = {
  # cabelo: loiros, mechas, iluminação sem descolorir, cor, corte, escova
  '002': (C, 'Retoque do loiro e corte'), '005': (C, 'Mechas inversas'), '006': (C, 'Corte personalizado'),
  '013': (C, 'Iluminado'), '014': (C, 'Morena iluminada sem descolorir'), '015': (C, 'Loiro gold'),
  '017': (C, 'Progressiva, raiz e tonalização'), '021': (C, 'Mechas rosa pink'), '029': (C, 'Loiríssima'),
  '033': (C, 'Iluminação sem descolorir'), '047': (C, 'Corte moderno'), '060': (C, 'Escova orgânica'),
  '079': (C, 'Loiro amanteigado'), '080': (C, 'Loiro perolado'), '081': (C, 'Iluminação sem descolorir'),
  '098': (C, 'Alinhamento para fios finos'), '120': (C, 'Loiro claríssimo'), '122': (C, 'Morena iluminada'),
  '153': (C, 'Iluminado e corte'), '156': (C, 'Iluminação sem descolorir'), '166': (C, 'Morena iluminada sem descolorir'),
  '170': (C, 'Retoque de raiz loiro'), '173': (C, 'Loiro e corte moderno'), '174': (C, 'Loiro e corte'),
  '181': (C, 'Vermelho e escova modelada'), '183': (C, 'Morena iluminada sem descolorir'), '249': (C, 'Loiro tratado'),
  '262': (C, 'Blond'), '294': (C, 'Descoloração global'), '295': (C, 'Super blond'), '317': (C, 'Mechas e corte'),
  '334': (C, 'Ruivo'), '353': (C, 'Iluminação sem descolorir'), '354': (C, 'Iluminação sem descolorir'),
  '376': (C, 'Mechas hot red'),
  # maquiagem
  '000': (M, 'Maquiagem'), '003': (M, 'Maquiagem'), '085': (M, 'Noiva'), '086': (M, 'Madrinha, make nude'),
  '087': (M, 'Make para o dia'), '130': (M, 'Maquiagem social'), '169': (M, 'Maquiagem'), '172': (M, 'Cabelo e make'),
  '178': (M, 'Make colorida'), '179': (M, 'Make iluminada'), '188': (M, 'Pele iluminada'), '189': (M, 'Make atemporal'),
  '190': (M, 'Maquiagem'), '191': (M, 'Noiva, 7 anos depois'), '257': (M, 'Make elegante'), '258': (M, 'Maquiagem'),
  '259': (M, 'Airbrush'), '266': (M, 'Pele jovem'), '267': (M, 'Pele madura'), '275': (M, 'Pele madura'),
  '307': (M, 'Noiva'), '314': (M, 'Noiva'), '320': (M, 'Formanda'), '321': (M, 'Make e escova modelada'),
  '322': (M, 'Formatura'), '323': (M, 'Noiva'), '328': (M, 'Maquiagem'), '134': (M, 'Make de carnaval'),
  # penteados e noivas
  '018': (P, 'Dia de noiva'), '091': (P, 'Make e penteado clássico'), '148': (P, 'Noiva clássica'),
  '161': (P, 'Make e penteado'), '177': (P, 'Penteado moderno'), '186': (P, 'Coque elegante'),
  '187': (P, 'Make e penteado'), '311': (P, 'Make e penteado'), '344': (P, 'Penteado'),
  '361': (P, 'Make e penteado'), '372': (P, 'Penteado'), '373': (P, 'Penteado'), '089': (P, 'Trança'),
}


def aparar(im, lim=22):
    """corta as faixas pretas (ou brancas) lisas de print de story em cima e embaixo"""
    g = im.convert('L')
    w, h = g.size
    def lisa(y):
        linha = g.crop((0, y, w, y + 1))
        lo, hi = linha.getextrema()
        return hi - lo < lim and (hi < 40 or lo > 225)
    t, b = 0, h
    while t < h // 3 and lisa(t):
        t += 1
    while b > h * 2 // 3 and lisa(b - 1):
        b -= 1
    return im.crop((0, t, w, b)) if (t or b < h) else im


def salvar(im, pasta, nome, larguras=(640, 1200), q=80):
    for w in larguras:
        c = im.copy()
        if c.width > w:
            c = c.resize((w, round(c.height * w / c.width)), Image.LANCZOS)
        c.save(os.path.join(pasta, f'{nome}-{w}.webp'), 'WEBP', quality=q, method=6)


def logo():
    """logo oficial (post 078): ouro sobre preto. Vira PNG/WebP com transparência:
    alfa = canal mais claro; cor = desmultiplicada pelo alfa."""
    im = Image.open(os.path.join(IG, '078.webp')).convert('RGB').crop((228, 924, 772, 1236))
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
    r, g, b = im.split()
    a = ImageChops.lighter(ImageChops.lighter(r, g), b).point(lambda v: 0 if v < 34 else min(255, int((v - 34) * 1.45)))
    px = im.load(); pa = a.load()
    out = Image.new('RGBA', im.size)
    po = out.load()
    for y in range(im.height):
        for x in range(im.width):
            al = pa[x, y]
            if al:
                cr, cg, cb = px[x, y]
                k = 255 / max(cr, cg, cb, 1)
                po[x, y] = (min(255, int(cr * k * .86)), min(255, int(cg * k * .78)), min(255, int(cb * k * .58)), al)
    out = out.crop(out.getbbox())
    out.save(os.path.join(IMG, 'logo-caverna.png'))
    # só o emblema (coroa + C), para favicon e para a versão horizontal
    em = out.crop((round(out.width * .345), 0, round(out.width * .655), round(out.height * .62)))
    em = em.crop(em.getbbox())
    # versão horizontal para o cabeçalho: emblema + "CAVERNA / HAIR E MAKEUP" lado a lado
    wm = out.crop((0, round(out.height * .635), out.width, out.height))
    wm = wm.crop(wm.getbbox())
    H = 400
    e2 = em.resize((round(em.width * H / em.height), H), Image.LANCZOS)
    w2 = wm.resize((round(wm.width * H * .62 / wm.height), round(H * .62)), Image.LANCZOS)
    hz = Image.new('RGBA', (e2.width + 60 + w2.width, H))
    hz.alpha_composite(e2, (0, 0))
    hz.alpha_composite(w2, (e2.width + 60, (H - w2.height) // 2 + 18))
    # cor sólida: champanhe escuro (fundo claro) e o dourado original (faixas escuras)
    def tingir(im, cor):
        t = Image.new('RGBA', im.size, cor + (0,))
        t.putalpha(im.split()[3])
        return t
    for nome, peca in (('logo-h', hz), ('logo', out)):
        for sufixo, im in (('', tingir(peca, CHAMPANHE)), ('-ouro', peca)):
            for w in ((240, 480) if nome == 'logo-h' else (360, 720)):
                im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(
                    os.path.join(IMG, f'{nome}{sufixo}-{w}.webp'), 'WEBP', quality=92, method=6)
    return out, em


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in glob.glob(os.path.join(OUT, '*.webp')):
        os.remove(f)
    lista = []
    for i in sorted(OBRAS):
        cat, desc = OBRAS[i]
        im = aparar(ImageOps.exif_transpose(Image.open(os.path.join(IG, i + '.webp'))).convert('RGB'))
        nome = f'ac-{i}'
        salvar(im, OUT, nome)
        lista.append({'id': nome, 'e': cat, 'd': desc, 'r': round(im.width / im.height, 3)})
    open(os.path.join(SITE, 'assets', 'js', 'obras.js'), 'w', encoding='utf-8').write(
        'window.OBRAS = ' + json.dumps(lista, ensure_ascii=False, separators=(',', ':')) + ';\n')

    lg, em = logo()

    # abertura: a foto dela com o espelho (post 076), sem o texto do lado
    h = Image.open(os.path.join(IG, '076.webp')).convert('RGB').crop((184, 330, 756, 1376))
    salvar(h, IMG, 'andreia-espelho', (480, 900), 84)
    # sobre e o espaço
    salvar(Image.open(os.path.join(IG, '031.webp')).convert('RGB').crop((0, 120, 1440, 1920)), IMG, 'andreia-retrato', (480, 900), 84)
    for n in ('066', '067'):
        salvar(aparar(Image.open(os.path.join(IG, n + '.webp')).convert('RGB')), IMG, 'espaco-' + n, (640,), 84)

    # favicon: emblema sobre preto
    for s, nome in ((32, 'favicon-32.png'), (180, 'assets/img/icone-180.png'), (512, 'assets/img/icone-512.png')):
        fav = Image.new('RGBA', (s, s), NUDE + (255,))
        e = Image.new('RGBA', em.size, CHAMPANHE + (0,)); e.putalpha(em.split()[3])
        lado = int(s * .78)
        e.thumbnail((lado, lado), Image.LANCZOS)
        fav.alpha_composite(e, ((s - e.width) // 2, (s - e.height) // 2))
        fav.convert('RGB').save(os.path.join(SITE, nome))
    Image.open(os.path.join(SITE, 'assets/img/icone-512.png')).save(os.path.join(SITE, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])

    # prévia de link 1200x630: logo no quadrado do meio (o WhatsApp recorta x 285–915), fotos nas laterais
    og = Image.new('RGB', (1200, 630), MARFIM)
    def arco(foto, x, w=210, hh=420, y=105, centro=(.5, .25)):
        """foto em arco, como na abertura do site, com um fio champanhe em volta"""
        f = ImageOps.fit(foto, (w, hh), Image.LANCZOS, centering=centro)
        m = Image.new('L', (w * 4, hh * 4), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 4 - 1, hh * 4 + w * 2), radius=w * 2, fill=255)
        og.paste(f, (x, y), m.resize((w, hh), Image.LANCZOS))
        ImageDraw.Draw(og).rounded_rectangle((x - 9, y - 9, x + w + 8, y + hh + w), radius=w // 2 + 9, outline=CHAMPANHE, width=2)
    og.paste(Image.new('RGB', (1200, 630 - 105 - 420), MARFIM), (0, 105 + 420))
    arco(h, 50)
    arco(Image.open(os.path.join(OUT, 'ac-015-1200.webp')).convert('RGB'), 1200 - 50 - 210, centro=(.5, .4))
    og.paste(Image.new('RGB', (1200, 630 - 105 - 420), MARFIM), (0, 105 + 420))
    l2 = Image.new('RGBA', lg.size, CHAMPANHE + (0,)); l2.putalpha(lg.split()[3])
    l2.thumbnail((560, 360), Image.LANCZOS)
    og.paste(l2, ((1200 - l2.width) // 2, (630 - l2.height) // 2 - 10), l2)
    og.save(os.path.join(SITE, 'og-caverna.jpg'), quality=86)
    print(len(lista), 'fotos')


if __name__ == '__main__':
    main()
