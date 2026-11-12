# Geradores de preparacao/

Geram, de fontes em Python, o material de cada aula no método da skill `aula-fonte-unica`: deck para o Gamma, roteiro, plano, figuras, guia do monitor, estudo dirigido, guia do professor, guia interativo e o guia geral da turma. Os textos da turma e do caso vêm de `turma.py`; nenhum gerador traz nome de turma, curso ou caso. Exemplo completo, da turma 2026.2-A: `assets/exemplo-2026-2-a/` do plugin.

`scripts/scaffold_preparacao.py <module.spec.yaml> <pasta_da_turma>` copia esta pasta para `<pasta_da_turma>/preparacao/` e escreve `turma.py` a partir do spec. Todos os comandos rodam na pasta da turma: `python -B preparacao/<gerador>.py <id>`, com `<id>` no formato `m3_a1`.

## Pasta da turma

```
<turma>/
  README.md                       tabela "Páginas publicadas": | M3 · 1 | <guia interativo> | <guia do monitor> |
  material-alunos/<CASO_PASTA>/   kit do caso: dados/, ferramentas/, tickets.json, prompts/
  M<m>/aula-<n>/                  saídas de cada aula
  preparacao/
    turma.py                      dados da turma e textos do guia geral
    aulas/<id>.py                 META, SLIDES, PARTE2, PLANO, ESTUDO, MONITOR
    professor/fala_<id>.py        USO, CASO, FALAS, PREPARO, ATOS, CONTINGENCIA, REFS, NOTA
    guias/conteudo_<id>.py        construir(ctx): o conteúdo do guia interativo
    guias/pedidos.json            pedidos exatos das execuções registradas
    guias/execucoes.json          saídas reais dessas execuções
```

## Ordem e o que cada um faz

`construir_tudo.py [ids]` roda, para cada aula de `turma.AULAS`, os passos 1 a 4. Os passos 5 a 8 rodam à parte.

| # | Gerador | Lê | Produz em `M<m>/aula-<n>/` | Recusa (sai com erro) quando |
|---|---|---|---|---|
| 1 | `construir_aula.py <id>` | `aulas/<id>.py`, `figuras.py` | `slides-gamma.md`, `gamma-colar.md`, `roteiro.md`, `plano.md`, `figuras/slide-NN.svg`, `figuras.html` | os `min` dos slides não somam `META["duracao"]`; falta campo no slide; título passa de 60 caracteres; slide sem fluxograma e sem `sem_fluxo`; fluxograma sem descrição ou com mais de 6 nós; rótulo que não cabe na figura |
| 2 | `exportar_figuras.py <id>` | `figuras/*.svg` | `figuras/slide-NN.png` em resolução dupla | não há SVG (rode o passo 1) |
| 3 | `construir_monitor.py <id>` | `MONITOR` e `SLIDES` | `guia-monitor.html` | falta o bloco `Monitor` ou `Mapa da aula` nos slides |
| 4 | `construir_estudo.py <id> [--sem-pdf]` | `ESTUDO` e os fluxogramas dos slides citados | `estudo-dirigido.html` e `.pdf` | — |
| 5 | `construir_professor.py <id>` | `aulas/<id>.py` e `professor/fala_<id>.py` | `guia-professor.html` | slide sem fala; fala fora de 3 a 5 parágrafos; passos de um ato que não somam o tempo do slide; comando de `PREPARO`, `ATOS` ou `CONTINGENCIA` que não está na `PARTE2` |
| 6 | `guias/gerar_guia.py <id>` | `guias/conteudo_<id>.py`, `pedidos.json`, `execucoes.json`, `material-alunos/<CASO_PASTA>/dados/`, `modelo.html`, `motor.js` com `agente_caso.js` | `guia-interativo.html` | bancada de tipo desconhecido; `motor.js` sem a linha `/*@inclui agente_caso.js*/` |
| 7 | `construir_guia_modulos.py` | todas as aulas, `turma.EMENTAS`, a tabela do `README.md`, `turma.GUIA_MODULOS` | `guia-modulos.html`, na pasta da turma | aula sem ementa ou sem link publicado; aula cuja grade difere da `noite.padrao` sem estar em `noite.excecoes` |
| 8 | `copiar_para_repositorio.py <clone>` | `material-alunos/<CASO_PASTA>/`, `estudo-dirigido.pdf` | cópia no clone, PDF com o nome de `turma.pdf_estudo` | o destino não é um clone git |

Os HTML abrem por duplo clique; o trecho entre `<!-- publicar:inicio -->` e `<!-- publicar:fim -->` é o corpo publicado como Artifact.

Auxiliares de `guias/`: `montar_experimentos.py` grava em `pedidos.json` os pedidos exatos das execuções; `registrar.py` grava em `execucoes.json` as saídas lidas das transcrições e confere se o pedido é idêntico; `extrair_corpo.py` separa o trecho publicável; `capturas.py` fotografa o guia em 1280 e 390 px e relata erros de JavaScript.

## O que muda de um caso para outro

- `turma.py`: todos os campos. Os textos de `GUIA_MODULOS` são da turma.
- `guias/agente_caso.js`: as ferramentas que o agente ao vivo do guia interativo recebe da página, imitando o servidor do caso, e `ligarAgente`, que as entrega ao modelo. `gerar_guia.py` insere o arquivo em `motor.js` no lugar da linha `/*@inclui agente_caso.js*/`. O arquivo é o do caso Balcão: reescreva as ferramentas para o caso novo e mantenha `ligarAgente(pref, ag)`, que `motor.js` chama.
- `guias/agente_caso.py`: o texto que descreve essas ferramentas no guia; muda junto com o `.js`.
- `guias/montar_experimentos.py`: `ferramentas_do_caso()` carrega o servidor MCP do caso e `pedidos_do_caso()` monta os pedidos de cada aula. Os dois são do Balcão: reescreva para o caso novo.
- `guias/pedidos.json` e `guias/execucoes.json` começam vazios.

## Requisitos

Python 3.12 ou mais novo; Playwright com Chromium (`python -m playwright install chromium`) para PNG, PDF e capturas; o SDK `mcp` para `montar_experimentos.py`. `guias/modelo.html` é cópia de `assets/modelo.html` da skill `guia-interativo-aula`: o guia usa só o `<style>` dele.
