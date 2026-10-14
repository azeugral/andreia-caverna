# Caverna Hair e Makeup

Site da Andréia Oliveira ([@andreiacaverna_hairemakeup](https://www.instagram.com/andreiacaverna_hairemakeup/)), cabeleireira e maquiadora em São Paulo há 14 anos.

Prévia: https://azeugral.github.io/andreia-caverna/ (com `noindex` até ter domínio).

## Identidade (v1, 14/10/2026)

Tirada do logo oficial dela (post "Ótimo início de semana", `../_ref/ig/078.webp`).

- **Cores:** preto `#0d0c0b`, ouro `#c9a35c` (claro `#e4c88f`) e marfim `#f1ebe1`.
- **Fontes:** Cinzel nos títulos (as mesmas capitulares romanas do "CAVERNA") e IBM Plex Sans no texto.
- **Logo:** recortado do post 078 e convertido para fundo transparente por `tools/processar.py`. O favicon é o emblema (coroa + C).
- **Layout:** logo centralizado no topo, barra de menu fixa embaixo dele (o logo pequeno aparece na barra ao rolar), seções simétricas.
- **Botões:** retos, com moldura dupla, como o anel em volta do C. No hover, o ouro claro entra pela esquerda.

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
