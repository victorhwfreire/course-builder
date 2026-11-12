# Exemplo: turma 2026.2-A

Referência para escrever as fontes de uma turma nova: as fontes da aula 1 do M3 da turma 2026.2-A de Sistemas com IA para Devs, copiadas sem alteração, e o `turma.py` dessa turma no formato do kit. Os geradores ficam em `../preparacao/`.

- `turma.py`: os dados da turma e os textos do guia geral (`GUIA_MODULOS`) preenchidos; com ele e as fontes originais, os geradores do kit reproduzem byte a byte as saídas da 2026.2-A.
- `aulas/m3_a1.py`: a fonte única de uma aula: `META`, `SLIDES` com fala, âncora, condução e fluxograma, `PARTE2`, `PLANO`, `ESTUDO` e `MONITOR`.
- `professor/fala_m3_a1.py`: o roteiro de fala slide a slide e o passo a passo da demonstração em dois atos, com os comandos que `construir_professor.py` confere contra a `PARTE2`.
- `guias/conteudo_m3_a1.py`: o conteúdo do guia interativo: conceitos com bancadas, demonstração com execuções registradas e o agente ao vivo.
- `material-alunos/caso-balcao/README.md`: o README do kit do caso, com o que cada arquivo é e em que aulas entra.
