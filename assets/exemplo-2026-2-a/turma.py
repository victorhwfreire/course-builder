"""Dados da turma 2026.2-A lidos pelos geradores de preparacao/."""
import re
import unicodedata

TURMA = "2026.2-A"
CURSO = "Sistemas com IA para Devs"
ORG = "CESAR School"
DOCENTE = "Victor Freire"
FERRAMENTA = "Claude Code"
CASO = "Balcão"
CASO_PASTA = "caso-balcao"
CASO_KIT = "dados, servidor MCP e scripts"
REPO = "https://github.com/victorhwfreire/sistemas_ia_devs_b2c_20262"
EMENTAS = ["../M3.md", "../M4.md"]
AULAS = ["m3_a1", "m3_a2", "m3_a3", "m4_a1", "m4_a2", "m4_a3"]

GUIA_MODULOS = {
    "lide": ("Seis aulas on-line, de {primeira} a {ultima}, às segundas e quartas, das 19h às 22h. O M3 dá autonomia e "
             "ferramentas ao modelo; o M4 mede, rastreia e protege o que foi construído. Um caso só, o suporte do Balcão, "
             "atravessa as seis aulas."),
    "agenda": "Seg e Qua · 19h–22h · on-line",
    "modulos": {"M3": "dá autonomia e ferramentas ao modelo", "M4": "mede, rastreia e protege o que foi construído"},
    "percurso": {
        "titulo": "Seis aulas em cadeia: cada uma usa o que a anterior construiu",
        "texto": ("Cada aula responde a uma pergunta. O M3 vai de decidir quem escolhe o próximo passo até plugar ferramentas "
                  "com limite; o M4 cobra a conta dessa autonomia: medir, explicar o custo e proteger."),
        "rotulo": "As seis aulas em ordem",
    },
    "noite": {
        "titulo": "Toda aula segue a mesma grade de três horas",
        "padrao": "m3_a2",
        "excecoes": ["m3_a1", "m4_a3"],
        "texto": ("O intervalo e o horário do monitor não mudam. Na primeira aula, a abertura vai até "
                  "{g[m3_a1][Abertura e mapa][fim]}, porque apresenta os módulos e o caso. Na última, a discussão tem "
                  "{g[m4_a3][Discussão][min]} minutos e o fechamento {g[m4_a3][Fechamento][min]}, porque ele também encerra o curso."),
        "blocos": {
            "Abertura e mapa": "Retomada da aula anterior e o mapa da noite: cinco conceitos e a pergunta que a aula responde.",
            "Conceitos": "Cinco conceitos em cadeia, cada um consequência do anterior, com um fluxograma por slide.",
            "Intervalo": "Quinze minutos, sempre no mesmo horário.",
            "Demonstração": ("Dois atos de 25 minutos no caso Balcão, com uma única mudança entre eles. O professor opera o "
                             "Claude Code; a turma assiste."),
            "Monitor": "Um monitor apresenta 20 minutos sobre um tema vizinho ao da aula.",
            "Discussão": "O professor apresenta os dois lados de uma questão e responde às perguntas do chat que o monitor resumiu.",
            "Fechamento": "O mapa refeito com o que a demonstração mostrou e a ponte para a próxima aula.",
        },
    },
    "caso": {
        "titulo": "Um caso só nas seis aulas: o suporte do Balcão",
        "texto": ("O Balcão é uma plataforma fictícia de pagamentos para pequenos comércios: maquininha, link de pagamento e "
                  "API. O suporte recebe tickets em texto livre e precisa classificar, investigar nos dados, agir e responder. "
                  "Cada aula olha para um pedaço desse fluxo."),
        "slide": ("m3_a1", "O caso Balcão"),
        "rotulo": "Fluxo do suporte do Balcão",
        "cartoes": [
            ("Os dados", ["12 tickets com gabarito de categoria, prioridade e time.",
                          "Clientes e cobranças, com cobranças duplicadas e tarifas contestadas de propósito.",
                          "A política de atendimento: categorias, prioridades P1 a P3 e as regras de estorno."]),
            ("As ferramentas", ["Um servidor MCP do Balcão, com contrato fraco e contrato forte.",
                                "O hook `guarda.py`, que nega estorno fora da política antes de a ferramenta rodar.",
                                "Scripts de triagem, de eval, do agente e de leitura de execução, todos em Python."]),
        ],
        "nota": (f"Tudo é fictício. O estorno do servidor é simulado: grava uma linha num arquivo. A pasta `caso-balcao` fica "
                 f"no repositório da turma: [{REPO[8:]}]({REPO})."),
    },
    "alunos": {
        "titulo": "Na aula você assiste; a prática vai no estudo dirigido",
        "cartoes": [
            ("Durante a aula", ["Não é preciso abrir nem executar nada: o professor explica e demonstra.",
                                "Ninguém é chamado pelo nome e a câmera não é pedida.",
                                "Às 19h, o monitor publica no chat os links do guia interativo e do repositório da turma.",
                                "O chat fica aberto o tempo todo. O monitor junta as perguntas e as leva ao professor na discussão."]),
            ("Depois da aula", ["O estudo dirigido de cada aula, em PDF, fica no repositório da turma, na pasta `estudos-dirigidos`: "
                                "conceitos detalhados, glossário, três práticas passo a passo no Claude Code, autoavaliação e leituras.",
                                "Reserve cerca de 3 horas por estudo, em uma ou duas sentadas.",
                                "O guia interativo revisa os cinco conceitos e mostra a demonstração com saídas reais registradas."]),
            ("Dúvidas", ["Na aula, no chat.",
                         "Entre as aulas, no canal da turma: os monitores respondem às dúvidas das práticas até a aula seguinte.",
                         "No dia seguinte a cada aula, o monitor publica no canal as dúvidas mais frequentes com resposta.",
                         "Nota e presença: com a coordenação."]),
        ],
        "preparo_titulo": "Prepare o computador uma vez, antes da primeira prática",
        "preparo": [
            ("**Claude Code instalado e com login.** O teste abaixo precisa responder `ok`. Se falhar, rode `claude` e faça `/login`.",
             'claude -p "responda apenas: ok"'),
            ("**Python 3.11 ou mais novo.**", "python --version"),
            (f"**O repositório da turma no seu computador.** Ele traz a pasta `caso-balcao`, usada em todas as práticas: "
             f"[{REPO[8:]}]({REPO}). Clone com o comando abaixo ou baixe o ZIP pelo botão Code da página. Os comandos das "
             f"práticas partem de `caso-balcao/ferramentas`, salvo quando o passo diz outra pasta.",
             f"git clone {REPO}.git"),
            ("**A partir da aula 2 do M3, o SDK do MCP.** Na pasta `caso-balcao`:", "pip install -r requirements.txt"),
            ("**No Windows PowerShell, acentos certos.** Rode antes dos scripts, em cada terminal novo:",
             '[Console]::OutputEncoding = [Text.Encoding]::UTF8; $env:PYTHONUTF8 = "1"'),
        ],
        "alerta": ("Custo e segurança nas práticas", [
            "O custo que o Claude Code mostra é estimativa. Na assinatura, não há cobrança por chamada.",
            "Um eval chama o modelo uma vez por ticket e por repetição: 12 tickets com 2 repetições são 24 chamadas.",
            "O estorno do servidor é simulado. Não aponte as ferramentas do caso para sistemas reais."]),
    },
    "monitores": {
        "titulo": "Um monitor por aula, com 20 minutos fixos às 21h15",
        "texto": ("Os monitores se revezam: cada aula tem um monitor responsável. Antes da aula, o professor envia o guia do "
                  "monitor daquela noite, com o fluxo minuto a minuto, os termos que você precisa dominar, as dúvidas prováveis "
                  "com resposta curta e um roteiro sugerido para a sua apresentação."),
        "cartoes": [
            ("Antes da aula", ["Ler o roteiro do professor e o estudo dirigido da aula.",
                               "Testar o próprio Claude Code com `claude -p \"responda apenas: ok\"`.",
                               "Rodar uma vez os scripts da demonstração no `caso-balcao`, para reconhecer a saída na tela do professor.",
                               "Deixar abertos o guia interativo, o PDF do estudo e o repositório da turma.",
                               "Combinar com o professor os sinais no chat privado: `5 min` para tempo e `P?` para pergunta pendente.",
                               "Ensaiar a apresentação com cronômetro."]),
            ("Depois da aula", ["No dia seguinte, publicar no canal as três dúvidas mais frequentes, com resposta.",
                                "Até a próxima aula, responder no canal às dúvidas das práticas do estudo dirigido.",
                                "Mandar ao professor, em duas linhas, o que funcionou e o que travou na apresentação."]),
        ],
        "durante": [
            ("Abertura", f"Publicar no chat, às 19h, os links do guia interativo e do repositório da turma, [{REPO[8:]}]({REPO}). "
                         "Responder dúvidas de acesso em privado."),
            ("Conceitos", "Separar as perguntas de conteúdo com o nome de quem perguntou. Responder no chat as dúvidas de "
                          "configuração (Claude Code, Python). Mandar `P?` no privado do professor quando houver pergunta boa."),
            ("Intervalo", "Avisar no chat que a volta é às 20h25 e escolher até três perguntas para a discussão."),
            ("Demonstração", "Deixar o guia interativo aberto na seção Demonstração: se o Claude Code do professor falhar, enviar "
                             "o link no chat. Avisar no privado se a fonte do terminal estiver ilegível."),
            ("Monitor", "Apresentar os 20 minutos. O professor cronometra e avisa aos 17."),
            ("Discussão", "Ler para o professor, em voz alta, até três perguntas do chat, cada uma resumida em uma frase."),
            ("Fechamento", "Publicar no canal da turma o PDF do estudo dirigido e o guia interativo. Lembrar a data da próxima aula."),
        ],
        "alerta": ("Combinados", [
            "A turma não é obrigada a falar: não chamar ninguém pelo nome nem pedir câmera.",
            "Nota e presença são com a coordenação.",
            "Não antecipar o conteúdo das próximas aulas. Se perguntarem, a resposta é a data em que o professor abre o assunto."]),
        "temas_texto": ("Cada guia traz um roteiro em quatro partes, com tempo, fontes e o que evitar. Use o caso Balcão nos "
                        "exemplos: a turma acompanha melhor quando o exemplo é o mesmo. O professor cronometra e avisa aos 17 minutos."),
    },
    "coordenacao": {
        "titulo": "O que muda nesta turma e o que cada aula entrega",
        "cartoes": [
            ("Formato", ["Aulas expositivas: só o professor opera, e nenhum momento depende de resposta da turma.",
                         "A prática que a ementa prevê em cada aula foi para o estudo dirigido, que cada aluno faz depois, no "
                         "Claude Code, com passo a passo.",
                         "Um monitor apresenta 20 minutos por aula, em horário fixo."]),
            ("Stack", ["A ementa prevê Python, orquestração (LangChain ou LangGraph) e um provider definido para a turma.",
                       "Nesta turma, o provider é o Claude, pelo Claude Code com a licença dos alunos. Os scripts do caso são em Python.",
                       "LangGraph é o tema sugerido ao monitor da primeira aula."]),
            ("Materiais de cada aula", ["Deck, roteiro de fala e plano com tabela de tempos, para o professor.",
                                        "Estudo dirigido em PDF, para os alunos.",
                                        "Guia do monitor e guia interativo, publicados como páginas.",
                                        "O kit do caso Balcão, comum às seis aulas."]),
        ],
    },
    "links_texto": f"**Repositório da turma.** O kit do caso Balcão, que as práticas dos estudos dirigidos usam: [{REPO[8:]}]({REPO}).",
}


def pdf_estudo(meta):
    """Caminho do estudo dirigido no repositório: estudos-dirigidos/m3-1-workflow-ou-agente.pdf."""
    tema = unicodedata.normalize("NFKD", meta["titulo"].split(":")[0]).encode("ascii", "ignore").decode().lower()
    return f"estudos-dirigidos/{meta['id'].replace('_a', '-')}-{re.sub(r'[^a-z0-9]+', '-', tema).strip('-')}.pdf"
