---
name: aula-fonte-unica
description: Contrato do modo estudo-dirigido do course-builder. Cada aula tem uma fonte única em Python (META, SLIDES, PARTE2, PLANO, ESTUDO, MONITOR), da qual geradores determinísticos produzem deck, roteiro, plano, figuras, estudo dirigido em PDF e guias HTML. Use ao escrever ou revisar qualquer fonte em preparacao/ (aulas/<id>.py, professor/fala_<id>.py, guias/conteudo_<id>.py) ou ao rodar os geradores.
---

# aula-fonte-unica

Método com que foram produzidas as seis aulas de M3 e M4 da turma 2026.2-A de Sistemas com IA para Devs (CESAR School, nov/2026). Na raiz do plugin (dois níveis acima da pasta desta skill), os exemplos completos estão em `assets/exemplo-2026-2-a/` e os geradores em `assets/preparacao/`; o `README.md` dessa pasta diz o que cada gerador lê, produz e confere. `scripts/scaffold_preparacao.py <spec> <saida>` copia os geradores para um módulo novo e escreve `turma.py` a partir do spec.

## 1. Princípios

- **Uma fonte por aula; nunca editar o que é gerado.** Para mudar uma aula, edite `preparacao/aulas/<id>.py` (ou a fala, ou o conteúdo do guia) e rode o gerador de novo. Arquivo `.md`, `.html` ou `.pdf` editado à mão é sobrescrito e some.
- **Aula expositiva.** Só o professor demonstra; nenhum momento depende de resposta da turma. A prática vai para o estudo dirigido, assíncrono.
- **Um caso fictício atravessa todas as aulas**, com um kit executável em `material-alunos/<caso.pasta>/`. Toda demonstração e toda prática usam esse kit.
- **Nada inventado.** Saída de modelo mostrada em material vem de execução real, registrada em `preparacao/guias/execucoes.json`, com o pedido exato em `pedidos.json`, data, modelo e a forma como foi obtida. Em 2026.2-A, as saídas do guia interativo vieram de subagentes do Claude Code, cada um numa conversa nova, sem ferramentas, com as definições das ferramentas do kit coladas no pedido e uma instrução de experimento no topo; `registrar.py` lê essas transcrições e confere que o pedido recebido é idêntico ao registrado. O ensaio das demonstrações roda os comandos da `PARTE2` de verdade. As duas formas valem desde que o material diga qual foi usada. Número de estudo entra com fonte primária e limite (modelos, tarefas, data). Frase que descreve a saída de um script é conferida contra o código do script.
- **Texto curto na tela, fluxograma em todo slide de conteúdo**: o título é a mensagem em uma frase; o corpo é um diagrama; a explicação vai para a fala.

## 2. Pastas (raiz = `out/<modulo>/`)

```
README.md                  mapa da turma, datas, monitores, "Antes de cada aula", "Como gerar de novo", páginas publicadas
guia-modulos.html          guia geral (alunos, monitores, coordenação)
material-alunos/<caso>/    kit do caso: README, entradas com gabarito (ex.: tickets.json), dados/, ferramentas/,
                           prompts/ quando uma aula compara instruções, requirements.txt (estado/ nasce ao rodar)
repo-turma/                base do repositório público da turma (README, .gitignore)
preparacao/
  turma.py                 TURMA, CURSO, ORG, DOCENTE, FERRAMENTA, CASO, CASO_PASTA, CASO_KIT, REPO, EMENTAS,
                           AULAS, GUIA_MODULOS (textos do guia geral), pdf_estudo()
  aulas/<id>.py            fonte única de cada aula
  professor/fala_<id>.py   fala completa do professor
  guias/conteudo_<id>.py   conteúdo do guia interativo; execucoes.json e pedidos.json
  kit-manifest.md          comandos do kit verificados (case-kit-builder)
  ensaio/<id>/             saídas brutas do ensaio de cada aula (demo-recorder)
  execucoes-relatorio.md   o que as execuções reais mostraram (demo-recorder)
<pasta da aula>/           slides-gamma.md, gamma-colar.md, roteiro.md, plano.md, figuras/, figuras.html,
                           estudo-dirigido.html e .pdf, guia-monitor.html, guia-interativo.html, guia-professor.html
```

`<id>` é `m<n>_a<k>` quando a aula tem `modulo` no spec (ex.: `m3_a1`, pasta `M3/aula-1`) e `a<k>` quando não tem (pasta `aulas/aula-<k>`).

## 3. Grade de uma aula de 180 min

| Bloco (`bloco` nos slides) | Minutos | 2026.2-A (19h–22h) |
|---|---:|---|
| Abertura e mapa | 10 (17 na primeira aula, que apresenta módulos, formato e caso) | 19h00–19h10 |
| Conceitos: cinco em cadeia, cada um consequência do anterior | 60 (53 na primeira) | até 20h10 |
| Intervalo fixo | 15 | 20h10–20h25 |
| Demonstração em dois atos de 25 min, mesmo caso, uma única mudança entre os atos | 50 | até 21h15 |
| Monitor: 20 min sobre um tema vizinho | 20 | 21h15–21h35 |
| Discussão: o professor apresenta os dois argumentos | 13 | 21h35–21h48 |
| Fechamento: refaz o mapa e responde à pergunta da aula | 12 | 21h48–22h00 |

Os horários de intervalo e monitor vêm de `spec.turma`; a soma dos `min` dos slides é igual a `META["duracao"]`.

## 4. `preparacao/aulas/<id>.py`

**`META`**: `id`, `pasta`, `curso`, `modulo`, `aula` ("M3 · Aula 1 de 3"), `titulo`, `data` ("Qua, 11/11/2026"), `inicio` ("19:00"), `duracao` (180), `docente`, `pergunta` (minúscula, com "?"), `roteiro_partes` (uma frase sobre as partes do roteiro), `links_roteiro` [(rótulo, caminho relativo)].

**`SLIDES`**: lista de dicionários. Obrigatórios: `bloco`, `min`, `titulo` (até 60 caracteres, uma frase que é a mensagem), `lede`, `fala` (resumo da fala, 3–5 frases), `ancora` (a frase que a turma leva), `conducao` (bastidor: o que fazer, o que não detalhar). Opcionais: `kicker` ("Conceito 2 de 5 · Agente"), `tela` [linhas curtas; `- ` vira lista], `fluxo`, `sem_fluxo: True` (só capa e intervalo).

**`fluxo`**: `forma` e `descricao` (versão em texto, obrigatória). No máximo 6 nós; rótulos que não cabem fazem o gerador falhar.
- `cadeia`: `nos` [nó…], `retorno` opcional (rótulo da seta de volta).
- `convergencia`: `entradas` (nó, nó), `saida` nó.
- `leque`: `entrada` nó, `saidas` [nó…], `faixa` (frase da faixa de baixo).
- `decisao`: `inicio` nó opcional, `pergunta` [linhas], `sim` [nó…], `nao` [nó…].
- `duas_faixas`: `rotulos` (r1, r2), `colunas` [(nó de cima, nó de baixo)…].
- Nó = `(título, apoio, tipo)`; `apoio` é str ou lista de até 2 linhas; `tipo`: `passo` (padrão, caixa cinza: etapa), `ia` (tracejada roxa: feita pelo modelo), `humano` (borda verde: decisão humana ou controle), `foco` (azul cheia: ponto de chegada). O losango amarelo é a decisão.

**`PARTE2`** (string Markdown crua): "Antes da aula" em checklist (teste de login que chama o modelo, cópia do kit para pasta curta, acentos no terminal, ensaio gravado em `C:\demo\ensaio\`); uma seção por ato com tabela `Tempo | O que fazer` que soma os minutos do slide, blocos ```` ```powershell ```` com os comandos exatos, "O que apontar" e falas condicionais "Se …" para cada comportamento que a execução real mostrou que pode variar; "Contingência" com o ensaio lido por um script que não chama o modelo e, por último, as saídas registradas do guia interativo, dizendo à turma de onde vieram.

**`PLANO`**: `formato`, `objetivo`, `resultados` [5], `ligacoes` [5, como cada conceito sai do anterior], `demo_resumo`, `atos` [(título, o que acontece, conceitos que mostra)], `fechamento` [monitor, discussão, fechamento, com horário e slide], `riscos` [falha → o que fazer].

**`ESTUDO`**: `tempo`, `objetivo`, `antes` [pré-requisitos com o teste de cada um], `conceitos` [{`titulo`, `definicao`, `texto` [parágrafos], `fig` (nº do slide cujo fluxograma ilustra), `exemplo` (no caso), `erro` (o equívoco comum), `pergunta` (pergunta, resposta)}], `glossario` [(termo, definição)], `praticas` [3 × {`titulo`, `tempo`, `objetivo`, `passos` [{`t`, `cmd` ou `prompt`, `obs`}], `observe` [], `pronto`, `extra`}], `autoavaliacao` [], `leituras` [(título, url, por que ler)]. Cada `cmd` roda no kit; cada `prompt` é o texto exato para a ferramenta base.

**`MONITOR`**: `resumo`, `termos`, `antes`, `durante`, `atencao`, `contribuir`, `duvidas`, `apresentacao` (roteiro dos 20 min em quatro partes, fontes, o que evitar), `depois`. Confira as chaves no exemplo `aulas/m3_a1.py`.

## 5. `preparacao/professor/fala_<id>.py`

`USO` [parágrafos], `CASO` (o caso em um parágrafo), `FALAS` {nº do slide: {`fala`: [3 a 5 parágrafos], `bastidor` opcional}}, `PREPARO` e `CONTINGENCIA` [{`titulo`, `texto`, `cmds` []}], `ATOS` [{`slide`, `titulo`, `passos` [{`min`, `titulo`, `fazer`, `cmds`, `tela`, `dizer`, `senao`}]}], `REFS` [referências completas], `NOTA` (limites dos números citados). Voz: skill `first-person-roteiro`; ações entre colchetes `[Rodar o workflow.]`. O gerador recusa slide sem fala, fala fora de 3–5 parágrafos, passos que não somam o `min` do slide e comando que não esteja na `PARTE2`.

## 6. Guia interativo

`preparacao/guias/conteudo_<id>.py` + `gerar_guia.py` + `motor.js`: os cinco conceitos com bancadas (passos, quiz, composto, custo, agente ao vivo com ferramentas da página), a demonstração com saídas registradas e botões que chamam o Claude ao vivo dentro do claude.ai. Saída registrada é marcada como tal, com data, modelo e como foi obtida; o rodapé diz o que é ilustrativo. As ferramentas da página imitam o kit e ficam isoladas em `guias/agente_caso.js` (com `ligarAgente`, que `motor.js` chama) e `guias/agente_caso.py` (o texto que as descreve): ao trocar de caso, reescreva esses dois e as funções `ferramentas_do_caso()` e `pedidos_do_caso()` de `guias/montar_experimentos.py`; `motor.js` não muda.

## 7. Gerar e conferir

Na raiz, nesta ordem: `construir_aula <id>`, `exportar_figuras <id>`, `construir_monitor <id>`, `construir_estudo <id>` (estes quatro são os que `construir_tudo.py` roda), depois `guias/gerar_guia <id>` e `construir_professor <id>`, e por fim `construir_guia_modulos`. Os três primeiros não leem `ESTUDO`, por isso a fonte pode ter `ESTUDO = {}` até o exercise-author escrever o estudo. Sempre `python -B`, com `PYTHONUTF8=1`. Gerador que sai com código 1 lista o que violou: corrija a fonte, não o gerador.

Antes de declarar uma aula pronta:
- todos os geradores passam;
- cada HTML abre por duplo clique (canônico autocontido, com `<!doctype html>` e `<meta charset="utf-8">`) e, em navegador real a 390 e 1280 px, não tem erro de página nem rolagem lateral;
- as páginas do PDF que mudaram foram abertas e olhadas;
- intervalo de caractere em regex usa escape (`\u00C0-\u00FF`), nunca literal acentuado.

## 8. Armadilhas que as execuções reais mostraram

- Windows PowerShell descarta um `--` sem aspas ao chamar o `claude.ps1` do npm: escreva `"--"` (ex.: `claude mcp add nome "--" python servidor.py`). No bash e no zsh as aspas não mudam nada.
- Acentos: `[Console]::OutputEncoding = [Text.Encoding]::UTF8` e `$env:PYTHONUTF8 = "1"` antes dos scripts.
- Login: `claude --version` não prova sessão; `claude -p "responda apenas: ok"` prova.
- Resposta completa de uma execução em stream-json: `(Get-Content x.jsonl -Encoding UTF8 | Select-Object -Last 1 | ConvertFrom-Json).result`. Resumo de script costuma cortar.
- `--max-budget-usd` é conferido depois da resposta: o gasto final pode passar do teto. Fins possíveis: `success`, `error_max_turns`, `error_max_budget_usd`; só `success` tem `result`.
- Em assinatura, o custo mostrado é estimativa do Claude Code, não cobrança.
- O modelo pode recusar sozinho o que a demonstração queria mostrar o controle negando: a fala tem de prever os dois caminhos, e a negação garantida é o teste do controle sem o modelo.
- Descrição de saída de script escrita de memória erra (ex.: "cortada em 24 caracteres" quando o código usa largura 34 e corta a categoria em 17): leia o código.
- Post ou resumo de terceiro não é a fonte do número: cite o artigo de onde o número saiu.
- Disco sincronizado (iCloud, OneDrive) deixa comandos lentos: rode em segundo plano.

## 9. Publicar (sempre depois do Gate HITL #2)

- Páginas viram Artifacts privados: o corpo publicável é extraído do canônico entre `<!-- publicar:inicio -->` e `<!-- publicar:fim -->` por `guias/extrair_corpo.py`, e `--comparar` prova que o publicado é o canônico. Compartilhar é decisão do usuário.
- O repositório da turma recebe o kit e os PDFs por `preparacao/copiar_para_repositorio.py <clone>`; commit e push só com aprovação explícita, nunca com force.
