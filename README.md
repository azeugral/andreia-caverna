# Caverna Hair e Makeup

Site da Andréia Oliveira ([@andreiacaverna_hairemakeup](https://www.instagram.com/andreiacaverna_hairemakeup/)), cabeleireira e maquiadora em São Paulo há 14 anos.

Prévia: https://azeugral.github.io/andreia-caverna/ (com `noindex` até ter domínio).

## Identidade (v2, 14/10/2026)

A v1 (preto chapado, capitulares romanas em Cinzel, moldura dourada nos botões) ficou com cara de barbearia. A v2 segue as referências de estúdios de cabelo e maquiagem "soft luxury": base clara, o dourado como champanhe só nos acentos e fotos em arco.

- **Cores:** marfim `#faf6f0`, nude `#f1e4da`, champanhe `#8c6a42` (o dourado do logo escurecido para ler no claro), rosé `#c99a87` nos detalhes e cacau `#2b211d` no texto, na faixa final e no rodapé.
- **Fontes:** Cormorant Garamond nos títulos e Jost no texto.
- **Logo:** o oficial, recortado do post 078 (`../_ref/ig/078.webp`). O `tools/processar.py` gera:
  - `logo-h-*`: versão horizontal (emblema + "CAVERNA / HAIR E MAKEUP") para o cabeçalho, em champanhe;
  - `logo-ouro-*`: o logo completo no dourado original, para o rodapé cacau;
  - favicon com o emblema champanhe sobre nude.
- **Cabeçalho:** o logo horizontal à esquerda e o menu à direita a partir de 1100 px. Abaixo disso aparecem o botão Agendar e uma gaveta de menu. Abaixo de 480 px, o "Menu" vira só ícone para tudo caber. O botão flutuante saiu, porque cobria os cards no celular.
- **Botões:** retos, cacau. No hover, o champanhe sobe de baixo.

## Estrutura

| Arquivo | O que é |
|---|---|
| `index.html` | Abertura, serviços, trabalhos recentes, dia de noiva, o estúdio, sobre, como agendar e chamada |
| `trabalhos.html` | Portfólio com filtro Cabelo, Maquiagem e Penteados (`?cat=`) e lightbox |
| `agendar.html` | Monta a mensagem e abre o WhatsApp. Aceita `?servico=escova`, `make`, `penteado`, `noiva` e `aula` |
| `assets/js/site.js` | `CONFIG` (Instagram e WhatsApp) e o comportamento do site |
| `assets/js/obras.js` | Gerado. Não editar à mão |

## Fluxo

```bash
python tools/processar.py      # fotos de ../_ref/ig -> assets/obras + obras.js, logo, fotos dela, favicons, og-caverna.jpg
python tools/montar_paginas.py # tools/paginas/*.html -> páginas da raiz (V = cache)
```

Os originais vieram do Instagram dela (540 posts mais recentes, em 13/10/2026). Estão em `../_ref/ig`, com as legendas em `../_ref/legendas.txt` e as folhas de contato em `../_ref/contato`.

## CONFIRMAR

Os itens pendentes aparecem no site como "✦ a preencher", com sublinhado tracejado.

- [ ] **DDD do WhatsApp:** o post mostra só 97226-0964. Usei 11 (São Paulo). Ajustar em `tools/montar_paginas.py` (ZAP), em `assets/js/site.js` (CONFIG) e no rodapé.
- [ ] **Bairro do estúdio e endereço.** Pelos posts, ela trabalhou no Tatuapé e deu aula na Vila Carrão (zona leste), mas o endereço do estúdio atual não aparece.
- [ ] **Horários de atendimento.**
- [ ] **Valores** dos serviços, ou se prefere "sob consulta".
- [ ] **Teste de maquiagem** para noivas: oferece?
- [ ] **Escova progressiva:** os posts falam em escova orgânica e progressiva "sem formol", mas um post de 2025 diz "com formol". O site só cita a escova orgânica. Confirmar antes de citar a progressiva.
- [ ] **Fernanda Takai e Erika Martins:** citadas no Sobre a partir de um post antigo em que ela maquia as duas. Confirmar se ela quer citar.
- [ ] **Fotos com texto de story:** algumas fotos do portfólio têm legendas escritas por cima (vieram de stories). Se ela tiver os originais, trocar.
- [ ] **Domínio:** quando houver, trocar `BASE` em `tools/montar_paginas.py`, tirar o `noindex` e trocar o `robots.txt`.
