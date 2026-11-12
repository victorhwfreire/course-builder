"""Dados da turma lidos pelos geradores de preparacao/. Troque cada <...>; exemplo preenchido: assets/exemplo-2026-2-a/turma.py do plugin course-builder."""
import re
import unicodedata

# Aparece nos rodapés como "Turma <TURMA>".
TURMA = "<código da turma, ex.: 2026.2-A>"
# Aparecem juntos como "<CURSO> · <ORG>".
CURSO = "<nome do curso>"
ORG = "<organização, ex.: CESAR School>"
DOCENTE = "<nome do professor>"
# Ferramenta das práticas do estudo dirigido.
FERRAMENTA = "Claude Code"
# O caso que atravessa as aulas; o kit dele fica em material-alunos/<CASO_PASTA>/.
CASO = "<nome do caso>"
CASO_PASTA = "<caso-slug>"
# O que o kit do caso traz, em poucas palavras; vai na tabela de materiais do plano.
CASO_KIT = "<ex.: dados, servidor MCP e scripts>"
# URL https do repositório da turma, ou "".
REPO = ""
# Relativas à pasta da turma. Cada ementa tem seções "## Aula 3.1 ..." com linhas "- Objetivo:" e "- Prática:".
EMENTAS = ["ementa.md"]
# Na ordem das aulas, no formato m<módulo>_a<aula>; cada id tem preparacao/aulas/<id>.py.
AULAS = []

# Textos do guia geral (construir_guia_modulos.py). Os textos aceitam `código`, **negrito** e [texto](https://...).
# "lide" aceita {primeira} e {ultima} (dd/mm da primeira e da última aula).
# "noite.texto" aceita {g[<id>][<bloco>][ini|fim|min]}: horário de início, de fim e minutos de um bloco da grade de uma aula.
GUIA_MODULOS = {
    "lide": "<quantas aulas, de {primeira} a {ultima}, dias e horário; o que cada módulo faz; o caso>",
    "agenda": "<ex.: Seg e Qua · 19h–22h · on-line>",
    "modulos": {"<M3>": "<o que o módulo faz, completando 'O M3 ...'>"},
    "percurso": {
        "titulo": "<frase sobre a sequência das aulas>",
        "texto": "<parágrafo: como uma aula leva à outra>",
        "rotulo": "<rótulo acessível da faixa de aulas, ex.: As seis aulas em ordem>",
    },
    "noite": {
        "titulo": "<frase sobre a grade de uma noite>",
        # Aula cuja grade é desenhada; as que diferem dela têm de estar em "excecoes" e ser explicadas no texto.
        "padrao": "<id>",
        "excecoes": [],
        "texto": "<o que não muda e por que as exceções diferem>",
        # Uma descrição por bloco da grade; Abertura e Mapa da aula viram "Abertura e mapa".
        "blocos": {
            "Abertura e mapa": "<...>",
            "Conceitos": "<...>",
            "Intervalo": "<...>",
            "Demonstração": "<...>",
            "Monitor": "<...>",
            "Discussão": "<...>",
            "Fechamento": "<...>",
        },
    },
    "caso": {
        "titulo": "<frase sobre o caso>",
        "texto": "<o que é a organização fictícia e que fluxo as aulas olham>",
        # (id da aula, início do título do slide) cujo fluxograma resume o caso.
        "slide": ("<id>", "O caso <nome>"),
        "rotulo": "<rótulo acessível do fluxo do caso>",
        "cartoes": [("Os dados", ["<...>"]), ("As ferramentas", ["<...>"])],
        "nota": "<o que é simulado e onde fica a pasta do caso>",
    },
    "alunos": {
        "titulo": "<frase sobre o papel do aluno>",
        "cartoes": [("Durante a aula", ["<...>"]), ("Depois da aula", ["<...>"]), ("Dúvidas", ["<...>"])],
        "preparo_titulo": "<ex.: Prepare o computador uma vez, antes da primeira prática>",
        # (texto do passo, comando copiável)
        "preparo": [("**<O que instalar.>** <como conferir>", "<comando>")],
        "alerta": ("Custo e segurança nas práticas", ["<...>"]),
    },
    "monitores": {
        "titulo": "<frase sobre o monitor e o horário fixo>",
        "texto": "<como funciona o rodízio e o que o monitor recebe>",
        "cartoes": [("Antes da aula", ["<...>"]), ("Depois da aula", ["<...>"])],
        # (bloco da aula, o que o monitor faz)
        "durante": [("Abertura", "<...>")],
        "alerta": ("Combinados", ["<...>"]),
        "temas_texto": "<como usar o roteiro do guia do monitor>",
    },
    "coordenacao": {
        "titulo": "<frase sobre o que muda nesta turma>",
        "cartoes": [("Formato", ["<...>"]), ("Stack", ["<...>"]), ("Materiais de cada aula", ["<...>"])],
    },
    "links_texto": "**Repositório da turma.** <o que há nele>",
}


def pdf_estudo(meta):
    """Caminho do estudo dirigido no repositório: estudos-dirigidos/m3-1-workflow-ou-agente.pdf."""
    tema = unicodedata.normalize("NFKD", meta["titulo"].split(":")[0]).encode("ascii", "ignore").decode().lower()
    return f"estudos-dirigidos/{meta['id'].replace('_a', '-')}-{re.sub(r'[^a-z0-9]+', '-', tema).strip('-')}.pdf"
