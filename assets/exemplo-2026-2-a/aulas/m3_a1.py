META = {
    "id": "m3_a1",
    "pasta": "M3/aula-1",
    "curso": "Sistemas com IA para Devs · CESAR School",
    "modulo": "M3 · Workflows, agentes, tool use e MCPs",
    "aula": "M3 · Aula 1 de 3",
    "titulo": "Workflow ou agente: quem decide o próximo passo",
    "data": "Qua, 11/11/2026",
    "inicio": "19:00",
    "duracao": 180,
    "docente": "Victor Freire",
    "pergunta": "quando vale dar autonomia ao modelo?",
    "roteiro_partes": (
        "A Parte 1 é a cronologia completa da aula. A Parte 2 detalha, com os comandos, a demonstração em dois atos "
        "dos slides 12 e 13; ela não soma tempo novo."
    ),
    "links_roteiro": [
        ("Plano da aula", "plano.md"),
        ("Texto dos slides", "slides-gamma.md"),
        ("Figuras", "figuras.html"),
        ("Guia do monitor", "guia-monitor.html"),
        ("Estudo dirigido", "estudo-dirigido.pdf"),
        ("Caso Balcão", "../../material-alunos/caso-balcao/README.md"),
    ],
}

SLIDES = [
    # ------------------------------------------------------------ Abertura
    {
        "bloco": "Abertura", "min": 2, "sem_fluxo": True,
        "titulo": "Workflow ou agente: quem decide o próximo passo",
        "lede": "M3 · Aula 1 de 3 — Workflows, agentes, tool use e MCPs",
        "tela": [
            "Sistemas com IA para Devs · CESAR School · Turma 2026.2-A",
            "Victor Freire · Quarta, 11/11/2026 · 19h–22h",
        ],
        "fala": (
            "Boa noite. Eu sou o Victor e fico com vocês nas próximas seis aulas, o M3 e o M4. No M1 e no M2 vocês "
            "viram como escolher o tipo de solução e como montar um RAG que responde com evidência. A partir de hoje "
            "o modelo deixa de só responder: ele passa a agir. E a primeira decisão de quem constrói esse tipo de "
            "sistema é quem decide o próximo passo, o código ou o modelo."
        ),
        "ancora": "A partir de hoje o modelo deixa de só responder e passa a agir.",
        "conducao": "Apresentação pessoal em uma frase. Antes das 19h, o monitor publica no chat os links do guia interativo e do repositório da turma, [github.com/victorhwfreire/sistemas_ia_devs_b2c_20262](https://github.com/victorhwfreire/sistemas_ia_devs_b2c_20262).",
    },
    {
        "bloco": "Abertura", "min": 3,
        "titulo": "M3 e M4: do agente que age ao sistema que se mede",
        "lede": "Seis aulas em cadeia. O M3 dá autonomia e ferramentas ao modelo; o M4 mede, rastreia e protege.",
        "fluxo": {
            "forma": "cadeia",
            "nos": [
                ("Workflow", ["ou agente?", "hoje"]),
                ("Tool use", ["contrato da", "ferramenta"]),
                ("MCP", ["integração, logs", "e limites"]),
                ("Evals", ["medir o", "comportamento"]),
                ("Logs e custo", ["rastrear cada", "execução"]),
                ("Guardrails", ["proteger e", "amadurecer"], "foco"),
            ],
            "descricao": (
                "Seis aulas em cadeia: workflow ou agente, hoje; tool use e o contrato da ferramenta; MCP com integração, "
                "logs e limites; evals para medir o comportamento; logs, custo e latência para rastrear cada execução; "
                "guardrails, fallback e maturidade para proteger e amadurecer."
            ),
        },
        "fala": (
            "O mapa das seis aulas. No M3, três passos: hoje, workflow ou agente; segunda, como dar uma ferramenta ao "
            "modelo sem ela quebrar; quarta que vem, como plugar ferramentas por um padrão, o MCP, com log e limite. "
            "No M4, o mesmo sistema passa pelo crivo de produção: medir se funciona, rastrear o que aconteceu e quanto "
            "custou, e proteger contra o que pode dar errado. Cada aula usa o que a anterior construiu."
        ),
        "ancora": "O M3 dá autonomia ao modelo; o M4 cobra a conta dessa autonomia.",
        "conducao": "Datas: M3 em 11, 16 e 18/11; M4 em 23, 25 e 30/11. Não detalhar o conteúdo do M4.",
    },
    {
        "bloco": "Abertura", "min": 3,
        "titulo": "Aqui vocês assistem; a prática vai no estudo dirigido",
        "lede": "Na aula, eu explico e demonstro. Depois, cada aula tem um estudo dirigido com conceitos e práticas passo a passo.",
        "fluxo": {
            "forma": "cadeia",
            "nos": [
                ("Exposição", ["conceitos", "em cadeia"]),
                ("Demonstração", ["eu opero,", "vocês assistem"]),
                ("Monitor", ["20 minutos sobre", "um tema vizinho"]),
                ("Estudo dirigido", ["PDF com práticas", "no Claude Code"], "foco"),
            ],
            "descricao": (
                "Formato de cada aula em quatro etapas: exposição dos conceitos em cadeia; demonstração em que o professor "
                "opera e a turma assiste; 20 minutos de um monitor sobre um tema vizinho; e, depois da aula, o estudo "
                "dirigido em PDF com práticas no Claude Code."
            ),
        },
        "fala": (
            "Como as aulas vão funcionar. Durante a aula, vocês não precisam abrir nada nem executar nada: eu explico, "
            "eu demonstro, e vocês acompanham. Em cada aula um monitor apresenta vinte minutos sobre um tema vizinho ao "
            "da noite. A prática fica para depois: cada aula tem um estudo dirigido, um PDF com os conceitos detalhados "
            "e práticas passo a passo, todas no Claude Code, que vocês já têm. O chat fica aberto o tempo todo; o "
            "monitor junta as perguntas e me passa nos momentos certos."
        ),
        "ancora": "Na aula vocês assistem; a mão na massa vai no estudo dirigido.",
        "conducao": (
            "Não pedir câmera nem resposta da turma. Os seis estudos dirigidos já estão no repositório da turma, pasta "
            "estudos-dirigidos; ao fim da aula o monitor lembra isso no canal. Se alguém perguntar sobre nota, remeter à coordenação."
        ),
    },
    {
        "bloco": "Abertura", "min": 4,
        "titulo": "O caso Balcão atravessa as seis aulas",
        "lede": "O Balcão é uma plataforma fictícia de pagamentos para pequenos comércios. O suporte recebe tickets e precisa triar e resolver.",
        "fluxo": {
            "forma": "cadeia",
            "nos": [
                ("Ticket", ["texto livre", "do cliente"]),
                ("Triagem", ["categoria", "e prioridade"]),
                ("Investigação", ["clientes, cobranças", "e política"]),
                ("Ação", ["nota, estorno", "ou encaminhamento"]),
                ("Resposta", "ao cliente", "foco"),
            ],
            "descricao": (
                "O fluxo do suporte do Balcão em cinco etapas: o ticket chega como texto livre do cliente; a triagem dá "
                "categoria e prioridade; a investigação consulta clientes, cobranças e política; a ação registra nota, "
                "emite estorno ou encaminha; e a resposta volta ao cliente."
            ),
        },
        "tela": ["12 tickets · clientes.json · cobrancas.json · politica-atendimento.md"],
        "fala": (
            "Para ninguém se perder trocando de exemplo, as seis aulas usam um caso só. O Balcão é uma plataforma "
            "fictícia de pagamentos para pequenos comércios: maquininha, link de pagamento, API. O suporte recebe "
            "tickets em texto livre, por exemplo: fui cobrada duas vezes da mensalidade em outubro. Alguém precisa "
            "classificar, investigar nos dados, decidir uma ação e responder. São doze tickets, um arquivo de clientes, "
            "um de cobranças e a política de atendimento. Hoje a pergunta é: esse fluxo é um workflow ou um agente?"
        ),
        "ancora": "Um caso só nas seis aulas: o suporte do Balcão.",
        "conducao": (
            "Mostrar a pasta material-alunos/caso-balcao no explorador por 30 segundos. Destacar o TCK-002, cobrança "
            "duplicada, que volta na demonstração e nas próximas aulas."
        ),
    },
    {
        "bloco": "Mapa da aula", "min": 5,
        "titulo": "Cinco conceitos em cadeia, uma pergunta no fim",
        "lede": "Cada conceito sai do anterior. Depois do intervalo, os cinco aparecem na tela, no caso Balcão.",
        "fluxo": {
            "forma": "cadeia",
            "nos": [
                ("1 · Workflow", ["o código decide", "o caminho"]),
                ("2 · Agente", ["o modelo decide", "o próximo passo"]),
                ("3 · Custo", ["cada passo é", "chance de errar"]),
                ("4 · Parada", ["limite escrito", "antes de rodar"]),
                ("5 · Escolha", ["workflow primeiro,", "agente com motivo"]),
                ("Pergunta", ["quando dar", "autonomia?"], "foco"),
            ],
            "descricao": (
                "Mapa da aula: cinco conceitos em cadeia. No workflow, o código decide o caminho; no agente, o modelo "
                "decide o próximo passo; cada passo a mais é uma chance a mais de errar; a política de parada é um "
                "limite escrito antes de rodar; e a escolha é workflow primeiro, agente com motivo. Termina na pergunta "
                "destacada: quando vale dar autonomia ao modelo?"
            ),
        },
        "fala": (
            "O mapa de hoje. Primeiro conceito: no workflow, quem decide o caminho é o código. Segundo, o contrário: "
            "no agente, quem decide o próximo passo é o modelo. Disso sai o terceiro: se o modelo decide quantos "
            "passos dar, cada passo a mais custa tempo, dinheiro e uma chance a mais de errar. O quarto é a resposta "
            "de engenharia a isso: uma política de parada escrita antes de rodar. E o quinto junta tudo numa regra de "
            "escolha. A pergunta que eu quero responder no fim é: quando vale dar autonomia ao modelo?"
        ),
        "ancora": "No fim de hoje: quando vale dar autonomia ao modelo?",
        "conducao": "Deixar a pergunta sem resposta; ela volta na discussão (slide 15) e é respondida no fechamento (slide 16).",
    },
    # ------------------------------------------------------------ Conceitos
    {
        "bloco": "Conceitos", "min": 12, "kicker": "Conceito 1 de 5 · Workflow",
        "titulo": "No workflow, o código decide o caminho",
        "lede": "Workflow é código que chama o modelo em passos fixos: a ordem, os desvios e o fim estão escritos antes de rodar.",
        "fluxo": {
            "forma": "cadeia",
            "nos": [
                ("Ticket", "texto do cliente"),
                ("Classificar", ["modelo: categoria", "e prioridade"], "ia"),
                ("Rotear", ["código: regra", "fixa por categoria"]),
                ("Responder", ["modelo: rascunho", "ao cliente"], "ia"),
                ("Fila do time", "sempre 3 passos", "foco"),
            ],
            "descricao": (
                "Workflow de triagem em cinco etapas: o ticket entra como texto; o modelo classifica categoria e "
                "prioridade; o código roteia por uma regra fixa por categoria; o modelo redige a resposta ao cliente; "
                "e o ticket chega à fila do time, sempre em três passos."
            ),
        },
        "tela": ["O modelo preenche os passos; quem escolhe o próximo passo é o código."],
        "fala": (
            "Começo pelo que vocês já conhecem, mesmo sem esse nome. O RAG do M2 é um workflow: buscar os trechos, "
            "montar o contexto, gerar a resposta. Sempre nessa ordem. Workflow é isso: código que chama o modelo em "
            "passos fixos. Na triagem do Balcão: uma chamada classifica o ticket em categoria e prioridade; uma regra "
            "no código manda para o time certo, sem modelo nenhum; outra chamada escreve o rascunho da resposta. O "
            "modelo trabalha dentro de cada caixa, mas a seta entre as caixas é do código.\n\n"
            "A Anthropic, num texto de 2024 que virou referência, chama isso de caminho predefinido e lista cinco "
            "padrões: encadear chamadas, rotear por tipo de entrada, paralelizar, um orquestrador distribuindo "
            "subtarefas e um avaliador que pede revisão. A nossa triagem é encadeamento com roteamento. O que esses "
            "padrões têm em comum é o que importa hoje: dá para desenhar o fluxo antes de rodar, e por isso dá para "
            "testar, prever o custo e explicar o que aconteceu."
        ),
        "ancora": "No workflow, o modelo trabalha dentro das caixas; as setas são do código.",
        "conducao": (
            "Fonte: Anthropic, “Building effective agents”, 19/12/2024 (workflows como caminhos de código "
            "predefinidos; cinco padrões). Não entrar em framework: LangGraph é o tema do monitor de hoje."
        ),
    },
    {
        "bloco": "Conceitos", "min": 11, "kicker": "Conceito 2 de 5 · Agente",
        "titulo": "No agente, o modelo escolhe o próximo passo",
        "lede": "Agente é um loop: o modelo olha o objetivo e o que já aconteceu, escolhe uma ação, recebe o resultado e decide de novo.",
        "fluxo": {
            "forma": "cadeia",
            "nos": [
                ("Objetivo", ["resolver o", "TCK-002"]),
                ("Modelo decide", ["a próxima ação", "ou parar"], "ia"),
                ("Ferramenta", ["lê, consulta", "ou executa"]),
                ("Resultado", ["entra na janela", "de contexto"], "foco"),
            ],
            "retorno": "repete até o modelo decidir parar",
            "descricao": (
                "Loop do agente: o objetivo, resolver o TCK-002, vai ao modelo, que decide a próxima ação ou parar; a "
                "ferramenta lê, consulta ou executa; o resultado entra na janela de contexto; e o ciclo se repete até "
                "o modelo decidir parar."
            ),
        },
        "tela": ["Mesmo modelo nos dois casos. Muda quem segura o volante."],
        "fala": (
            "Segundo conceito, o espelho do primeiro. Agora eu entrego ao modelo o objetivo, resolva o TCK-002, e "
            "algumas ferramentas: ler arquivos, consultar dados. Ele decide sozinho a próxima ação: talvez ler as "
            "cobranças, talvez a política primeiro. A ferramenta executa, o resultado entra na janela de contexto, "
            "aquela do M2, e o modelo decide de novo. Loop. Em código, é um while: enquanto o modelo não disser que "
            "terminou, chame o modelo, execute o que ele pediu e devolva o resultado.\n\n"
            "Esse padrão tem nome na pesquisa desde 2022, ReAct: raciocinar e agir em alternância. E vocês usam um "
            "agente desses todo dia: o Claude Code é exatamente isso, um modelo num loop com ferramentas de ler, "
            "editar e rodar comandos. Reparem que o modelo é o mesmo do workflow. O que muda é quem segura o volante. "
            "E quem segura o volante decide também quantas voltas a execução vai dar."
        ),
        "ancora": "Agente é um while: o modelo decide, a ferramenta executa, o resultado volta.",
        "conducao": (
            "Fonte: Yao et al., “ReAct: Synergizing Reasoning and Acting in Language Models”, arXiv:2210.03629 "
            "(ICLR 2023). Não detalhar o formato da chamada de ferramenta: é o tema da aula 2."
        ),
    },
    {
        "bloco": "Conceitos", "min": 11, "kicker": "Conceito 3 de 5 · Custo da autonomia",
        "titulo": "Cada passo a mais é uma chance a mais de errar",
        "lede": "Se cada passo acerta 95% das vezes, a execução inteira acerta menos a cada passo: o erro se acumula.",
        "fluxo": {
            "forma": "cadeia",
            "nos": [
                ("1 passo", "95% de acerto"),
                ("5 passos", "77% de acerto"),
                ("10 passos", "60% de acerto"),
                ("20 passos", "36% de acerto", "foco"),
            ],
            "descricao": (
                "Erro composto, ilustrativo: com 95% de acerto em cada passo independente, uma execução de 1 passo "
                "acerta 95%; de 5 passos, 77%; de 10 passos, 60%; de 20 passos, 36%."
            ),
        },
        "tela": ["Ilustrativo: passos independentes, 95% de acerto em cada um (0,95 elevado ao número de passos)."],
        "fala": (
            "Terceiro conceito, consequência direta do segundo. Se o modelo decide quantos passos dar, o número de "
            "passos vira variável, e cada passo cobra três coisas. Tempo: cada volta é mais uma chamada. Dinheiro: "
            "cada volta reenvia a janela inteira, que só cresce. E risco: se cada passo acerta 95% das vezes, cinco "
            "passos seguidos acertam 77%, dez passos acertam 60%, vinte, 36%. É conta de probabilidade, zero vírgula "
            "noventa e cinco elevado ao número de passos. Os passos reais não são independentes assim, mas a "
            "direção é essa: o erro se acumula.\n\n"
            "Tem um segundo efeito, e esse vocês vão ver na tela. O mesmo ticket, rodado duas vezes pelo agente, "
            "pode levar três passos numa execução e seis na outra. Então custo e tempo variam de uma execução para a "
            "outra. No workflow da triagem, são sempre duas chamadas ao modelo por ticket. Autonomia não é de graça: "
            "a gente paga em variação."
        ),
        "ancora": "Autonomia se paga em tempo, custo e erro que se acumula.",
        "conducao": (
            "A tabela é ilustrativa; dizer isso. Medir acerto com várias execuções (pass@k, pass^k) é tema do M4, "
            "aula 1. Não citar números de benchmark."
        ),
    },
    {
        "bloco": "Conceitos", "min": 10, "kicker": "Conceito 4 de 5 · Política de parada",
        "titulo": "Todo agente precisa de uma política de parada",
        "lede": "Política de parada é a regra, escrita antes de rodar, de quando o loop termina: objetivo cumprido, limite atingido ou passagem para uma pessoa.",
        "fluxo": {
            "forma": "decisao",
            "inicio": ("Fim da volta", "a cada passo"),
            "pergunta": ["Cumpriu a meta", "ou bateu limite?"],
            "sim": [("Para", ["entrega ou passa", "a uma pessoa"], "foco")],
            "nao": [
                ("Progrediu?", ["algo novo", "na janela"], "humano"),
                ("Nova volta", "o modelo decide", "ia"),
            ],
            "descricao": (
                "Decisão ao fim de cada volta: cumpriu a meta ou bateu um limite? Se sim, para: entrega a resposta "
                "ou passa a uma pessoa. Se não, verifica se progrediu, com algo novo na janela; com progresso, uma "
                "nova volta em que o modelo decide."
            ),
        },
        "tela": ["No Claude Code em modo não interativo: --max-budget-usd e --max-turns limitam a execução."],
        "fala": (
            "Quarto conceito, a resposta de engenharia ao terceiro. Se cada volta custa e arrisca, alguém precisa "
            "decidir quando o loop termina, e esse alguém não pode ser só o modelo. Política de parada é essa regra, "
            "escrita antes de rodar. Ela tem cinco campos: o objetivo verificável, ou seja, como eu sei que terminou; "
            "um teto de passos; um teto de custo; um teto de tempo; e a condição de passar para uma pessoa, por "
            "exemplo, duas voltas sem nada novo, ou uma ação sensível como um estorno.\n\n"
            "No Claude Code isso já existe em forma de opção. Rodando sem interação, com menos p, eu posso limitar o "
            "gasto em dólares e o número de voltas. Na demonstração eu vou rodar o agente com teto de cinquenta "
            "centavos de dólar. Reparem no que a política não faz: ela não deixa o agente mais inteligente. Ela "
            "garante que, quando ele errar, o erro tem tamanho máximo."
        ),
        "ancora": "A política de parada não deixa o agente mais esperto; ela limita o tamanho do erro.",
        "conducao": (
            "Opções conferidas na referência da CLI do Claude Code (code.claude.com/docs): --max-budget-usd e "
            "--max-turns valem só no modo -p. O gasto pode passar um pouco do teto: o corte acontece depois da "
            "chamada que cruzou o limite."
        ),
    },
    {
        "bloco": "Conceitos", "min": 9, "kicker": "Conceito 5 de 5 · Síntese",
        "titulo": "Comece pelo workflow; suba para agente com motivo",
        "lede": "Se dá para escrever os passos antes, é workflow. Se o caminho depende do que se descobre no meio, é agente, com limites.",
        "fluxo": {
            "forma": "decisao",
            "inicio": ("Problema", "um tipo de ticket"),
            "pergunta": ["Dá para escrever", "os passos antes?"],
            "sim": [("Workflow", ["previsível, barato", "e testável"], "foco")],
            "nao": [
                ("Agente", "com ferramentas", "ia"),
                ("Com limites", ["parada, custo", "e registro"], "humano"),
            ],
            "descricao": (
                "Decisão de síntese: para um problema, como um tipo de ticket, dá para escrever os passos antes? Se "
                "sim, workflow: previsível, barato e testável. Se não, agente com ferramentas, sempre com limites de "
                "parada, custo e registro."
            ),
        },
        "fala": (
            "O quinto conceito junta os quatro numa pergunta: dá para escrever os passos antes de rodar? Para uma "
            "dúvida de produto, como emitir relatório por bandeira, dá: classificar, responder com o artigo certo, "
            "fim. Workflow. Para uma cobrança que o cliente contesta, o caminho depende do que aparece no meio: tem "
            "duplicidade? É tarifa? Tinha contrato? Aí o agente se paga, porque ninguém escreveria todos os desvios "
            "antes. E mesmo assim, com política de parada e com registro do que ele fez.\n\n"
            "Muita equipe faz o contrário: começa pelo agente porque impressiona na demo, e descobre o custo e a "
            "variação em produção. A regra é começar pelo mais simples que resolve e subir de degrau quando houver "
            "motivo. Depois do intervalo, eu mostro os dois rodando no mesmo caso."
        ),
        "ancora": "Workflow quando dá para escrever o caminho; agente quando o caminho se descobre, sempre com limite.",
        "conducao": (
            "A recomendação de começar simples está no mesmo texto da Anthropic de 2024. Ferramentas e contratos ficam "
            "para a aula 2; integração e permissões, para a aula 3."
        ),
    },
    # ------------------------------------------------------------ Intervalo
    {
        "bloco": "Intervalo", "min": 15, "sem_fluxo": True,
        "titulo": "Intervalo",
        "lede": "Voltamos às 20h25 para ver os cinco conceitos acontecendo.",
        "fala": "Quinze minutos. Às 20h25 a gente volta com o workflow e o agente rodando no mesmo caso.",
        "ancora": "Na volta, os dois rodando no mesmo caso.",
        "conducao": "O intervalo não desliza: atraso sai da discussão. Abrir o terminal em C:\\demo\\caso-balcao\\ferramentas (Parte 2).",
    },
    # ------------------------------------------------------------ Demonstração
    {
        "bloco": "Demonstração", "min": 25, "kicker": "Demonstração · Ato 1 de 2",
        "titulo": "Ato 1: o workflow faz sempre os mesmos passos",
        "lede": "Tarefa: triar tickets do Balcão. Condição: o código fixa os passos; o modelo só classifica e redige.",
        "fluxo": {
            "forma": "cadeia",
            "nos": [
                ("Rodar o script", ["3 tickets,", "1 comando"]),
                ("Classificar", ["saída em JSON", "com esquema"], "ia"),
                ("Rotear", ["código,", "sem modelo"]),
                ("Responder", ["rascunho", "ao cliente"], "ia"),
                ("Mesmo caminho", ["2 chamadas", "por ticket"], "foco"),
            ],
            "descricao": (
                "Ato 1 em cinco etapas: rodar o script em três tickets com um comando; o modelo classifica com saída em "
                "JSON validada por esquema; o código roteia sem modelo; o modelo redige o rascunho ao cliente; e a "
                "chegada é o mesmo caminho em todo ticket, duas chamadas ao modelo por ticket."
            ),
        },
        "tela": ["Conceitos à vista: 1 workflow · 3 custo e tempo previsíveis"],
        "fala": (
            "Agora os conceitos acontecendo. Primeiro ato: o workflow. O script tem três passos fixos e cada chamada "
            "ao modelo é feita pelo próprio Claude Code em modo não interativo, com menos p, que devolve um JSON com a "
            "resposta, o tempo e o custo estimado. Abro o código: aqui a chamada que classifica, com um esquema que "
            "obriga a resposta a ser uma categoria e uma prioridade da lista; aqui o roteamento, um dicionário do "
            "Python; aqui a chamada que escreve a resposta. Rodo em três tickets: a maquininha parada, a cobrança "
            "duplicada e a farmácia que recebeu menos do que vendeu.\n\n"
            "Reparem na tabela: duas chamadas ao modelo por ticket, sempre. Tempo e custo parecidos de um ticket para "
            "o outro. Conceito um: o caminho é do código. Conceito três, pelo lado bom: dá para prever o custo de mil "
            "tickets multiplicando. E reparem também no limite: o workflow classificou a farmácia, mas não "
            "investigou nada. Ele não sabe se foi tarifa ou erro, porque investigar não estava nos passos."
        ),
        "ancora": "Workflow: mesmo caminho, custo previsível, e só faz o que estava escrito.",
        "conducao": (
            "Comandos e contingências na Parte 2. Se uma classificação divergir do gabarito, mostrar sem corrigir: é "
            "exatamente o que o M4 vai medir com eval. Não discutir prompt engineering."
        ),
    },
    {
        "bloco": "Demonstração", "min": 25, "kicker": "Demonstração · Ato 2 de 2",
        "titulo": "Ato 2: o agente escolhe o que investigar",
        "lede": "Mesmo caso, ticket TCK-002. Condição: o Claude Code lê os dados do Balcão e decide o que consultar, com teto de US$ 0,50.",
        "fluxo": {
            "forma": "cadeia",
            "nos": [
                ("Pedido", ["objetivo e pasta", "de dados"]),
                ("Decide ler", ["cobranças?", "política?"], "ia"),
                ("Confere", ["dois lançamentos", "de R$ 189,90"], "ia"),
                ("Roda de novo", ["compara passos", "e resposta"], "ia"),
                ("Registro", ["passos, tempo", "e custo"], "foco"),
            ],
            "descricao": (
                "Ato 2 em cinco etapas: o pedido traz o objetivo e a pasta de dados; o agente decide o que ler, "
                "cobranças ou política; confere os dois lançamentos de R$ 189,90; a mesma tarefa é rodada de novo "
                "para comparar passos e resposta; e a chegada é o registro de passos, tempo e custo."
            ),
        },
        "tela": ["Conceitos à vista: 2 loop do agente · 3 variação de custo · 4 política de parada"],
        "fala": (
            "Segundo ato: mesmo caso, agora com o agente. O pedido diz o objetivo, resolver o TCK-002, e onde estão "
            "os dados. Eu libero só leitura: ler, listar e buscar arquivos, nada de editar. E coloco o teto de "
            "cinquenta centavos de dólar. Rodo, e o registro da execução mostra o loop, conceito dois: ele decidiu "
            "listar a pasta, ler os arquivos, achou dois lançamentos de cento e oitenta e nove e noventa no mesmo dia, "
            "conferiu a política de estorno e só então escreveu a resposta. Ninguém escreveu esses passos.\n\n"
            "Rodo de novo, o mesmo pedido, e comparo os dois resumos, conceito três. Com dados pequenos como os "
            "nossos, o caminho pode até se repetir; aí a variação aparece no texto da resposta e no custo, que vira "
            "uma faixa. E para mostrar o conceito quatro, rodo o ticket da farmácia com um teto baixo, cinco "
            "centavos: a execução para no limite, com o motivo registrado. Comparem com o primeiro ato: o agente "
            "investigou o que o workflow não investigava, e cobrou por isso em variação."
        ),
        "ancora": "O agente investigou o que ninguém escreveu, e cobrou em variação.",
        "conducao": (
            "Ler o registro com ler_execucao.py, não o JSON cru. Se o agente ler um arquivo a mais ou a menos, ótimo: "
            "é a variação. Se ele tentar editar algo, mostrar a negação no registro: só a leitura foi liberada. Nas "
            "duas execuções registradas em 10/11 para o guia, o caminho foi igual (listou a pasta e leu os três "
            "arquivos de uma vez) e o agente achou, sem o pedido mandar, a mesma duplicidade no Bazar Estrela e as "
            "tarifas sem contrato da Loja Bela Casa: usar como exemplo do que o workflow não faria."
        ),
    },
    # ------------------------------------------------------------ Monitor
    {
        "bloco": "Monitor", "min": 20, "sem_fluxo": True,
        "titulo": "Com a palavra, o monitor: o caso Balcão em LangGraph",
        "lede": "Vinte minutos sobre como um framework representa workflow e agente como grafo de estados.",
        "tela": [
            "- **Estado, nós e arestas** — o vocabulário do grafo",
            "- **O workflow da triagem como grafo** — aresta condicional no lugar do dicionário",
            "- **O agente como grafo com volta** — nó do modelo, nó das ferramentas e limite de recursão",
        ],
        "fala": (
            "Agora eu passo a palavra ao monitor. Hoje eu mostrei workflow e agente com um script e com o Claude Code. "
            "Na indústria, muita gente monta esses dois desenhos com um framework, e o mais usado no ecossistema Python "
            "é o LangGraph. O monitor vai mostrar o nosso caso como grafo."
        ),
        "ancora": "O mesmo desenho, agora como grafo de estados.",
        "conducao": (
            "Cronometrar 20 minutos e avisar aos 17. Roteiro sugerido da apresentação no guia do monitor. Se o "
            "monitor não puder apresentar, usar o tempo para ler o código de workflow_triagem.py e rodar_agente.py."
        ),
    },
    # ------------------------------------------------------------ Discussão
    {
        "bloco": "Discussão", "min": 13,
        "titulo": "Investigar ou repetir: o que pesa mais?",
        "lede": "Dois argumentos sobre o que a demonstração mostrou, e a pergunta da aula.",
        "fluxo": {
            "forma": "convergencia",
            "entradas": [
                ("Argumento A", ["o agente achou a", "duplicidade sozinho"]),
                ("Argumento B", ["o workflow repetiu", "igual e custou menos"]),
            ],
            "saida": ("Pergunta", ["quando vale dar", "autonomia ao modelo?"], "foco"),
            "descricao": (
                "Dois argumentos convergem na pergunta da aula. Argumento A: o agente achou a duplicidade sozinho. "
                "Argumento B: o workflow repetiu igual e custou menos. Pergunta: quando vale dar autonomia ao modelo?"
            ),
        },
        "fala": (
            "Eu mesmo vou defender os dois lados. Argumento A: o agente achou a duplicidade sozinho, conferiu a "
            "política e escreveu uma recomendação que o workflow não teria. Para ticket de cobrança, isso economiza o "
            "tempo de uma pessoa. Argumento B: o workflow fez sempre a mesma coisa, custou menos e eu consigo testar e "
            "explicar cada passo. Para dúvida de produto, investigar é desperdício. Os dois estão certos, para tipos "
            "diferentes de ticket. Por isso a decisão não é da equipe nem da ferramenta: é de cada tipo de problema. "
            "Se no chat tiver alguma pergunta, o monitor traz agora."
        ),
        "ancora": "A decisão é por tipo de problema, não por time nem por ferramenta.",
        "conducao": (
            "Ler no máximo três perguntas do chat que o monitor separou. Sem pergunta, mostrar o desenho híbrido: um "
            "workflow que roteia e chama o agente só na categoria cobranca_indevida. Não fechar a resposta: é do slide 16."
        ),
    },
    # ------------------------------------------------------------ Fechamento
    {
        "bloco": "Fechamento", "min": 12,
        "titulo": "Autonomia é decisão de projeto, não upgrade",
        "lede": "O mapa da aula em uma frase por conceito.",
        "fluxo": {
            "forma": "cadeia",
            "nos": [
                ("Workflow", ["o código decide", "o caminho"]),
                ("Agente", ["o modelo decide", "o próximo passo"], "ia"),
                ("Custo", ["erro e variação", "se acumulam"]),
                ("Parada", ["limite escrito", "antes de rodar"], "humano"),
                ("Escolha", ["por tipo de", "problema"]),
                ("Resposta", ["quando o caminho", "se descobre"], "foco"),
            ],
            "descricao": (
                "O mapa refeito em uma frase por conceito: no workflow o código decide o caminho; no agente o modelo "
                "decide o próximo passo; erro e variação se acumulam; a parada é um limite escrito antes de rodar; a "
                "escolha é por tipo de problema. A resposta à pergunta da aula: dar autonomia quando o caminho se "
                "descobre no meio."
            ),
        },
        "tela": [
            "Estudo dirigido da aula 1 no canal da turma: três práticas no Claude Code.",
            "Segunda, 16/11: tool use e function calling — como dar uma ferramenta ao modelo sem ela quebrar.",
        ],
        "fala": (
            "Voltando à pergunta: quando vale dar autonomia ao modelo? Quando o caminho se descobre no meio e não dá "
            "para escrever os passos antes. Fora disso, workflow. E quando for agente, com política de parada e "
            "registro. O estudo dirigido de hoje tem três práticas: montar o workflow de triagem, rodar o mesmo ticket "
            "como agente e comparar, e escrever a política de parada de um agente do trabalho de vocês. Na segunda a "
            "gente abre a caixa da ferramenta: o que faz uma ferramenta ser boa para um modelo."
        ),
        "ancora": "Dar autonomia quando o caminho se descobre; fora disso, workflow.",
        "conducao": (
            "O monitor publica o estudo dirigido em PDF e o guia interativo no canal ao fim da aula. Anotar o tempo "
            "real de cada momento para ajustar as próximas aulas."
        ),
    },
]

PARTE2 = r"""
## Parte 2 — Demonstração em dois atos, com os comandos

Mesmo caso nos dois atos: a fila de suporte do Balcão. No Ato 1 o código decide os passos; no Ato 2 o modelo decide. Só o professor opera; a turma assiste.

### Antes da aula

- [ ] Claude Code autenticado: `claude -p "responda apenas: ok"` precisa responder `ok`. `claude --version` não basta. Se aparecer “OAuth session expired”, rodar `claude`, entrar com `/login` e testar de novo.
- [ ] Python 3.11 ou mais novo (`python --version`). Esta aula não precisa de pacote extra.
- [ ] Cópia do caso numa pasta curta e terminal com acentos:

```powershell
Remove-Item -Recurse -Force C:\demo\caso-balcao -ErrorAction SilentlyContinue
Copy-Item -Recurse -Force "$HOME\iCloudDrive\Trabalho\CESAR\Aulas\Sistemas-IA-para-Devs\2026.2-A\material-alunos\caso-balcao" C:\demo\
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$env:PYTHONUTF8 = "1"
cd C:\demo\caso-balcao\ferramentas
```

- [ ] Fonte do terminal ampliada; `workflow_triagem.py` aberto no editor ao lado.
- [ ] Ensaiar os dois atos e guardar as saídas em `C:\demo\ensaio\`: são a contingência se a rede cair. Anotar tempo, custo e voltas de cada execução.

```powershell
New-Item -ItemType Directory -Force C:\demo\ensaio | Out-Null
python workflow_triagem.py TCK-001 TCK-002 TCK-011 | Tee-Object C:\demo\ensaio\ato1.txt
python rodar_agente.py --ticket TCK-002 --modo arquivos --saida C:\demo\ensaio\ato2-1.jsonl
python rodar_agente.py --ticket TCK-002 --modo arquivos --saida C:\demo\ensaio\ato2-2.jsonl
python rodar_agente.py --ticket TCK-011 --modo arquivos --orcamento 0.05 --saida C:\demo\ensaio\ato2-teto.jsonl
```

### Slide 12 — Ato 1: workflow (25 min)

| Tempo | O que fazer |
|---:|---|
| 4 min | Mostrar no editor os três passos de `workflow_triagem.py`: a chamada com `--json-schema`, o dicionário `ROTA`, a chamada que redige. |
| 3 min | Mostrar uma chamada isolada e o JSON que ela devolve (`result`, `structured_output`, `duration_ms`, `total_cost_usd`). |
| 8 min | Rodar o workflow em três tickets e ler a tabela. |
| 5 min | Rodar a classificação do TCK-011 duas vezes sem a resposta: o caminho é o mesmo. Se o rótulo variar, é o gancho do M4; nas execuções registradas em 10/11, deu `cobranca_indevida`/P2 nas duas. |
| 5 min | Fechar o ato: caminho fixo, custo previsível, e a farmácia ficou sem investigação. |

```powershell
claude -p "Classifique este ticket em uma palavra: maquininha não passa débito desde as 9h." --output-format json
python workflow_triagem.py TCK-001 TCK-002 TCK-011
python workflow_triagem.py TCK-011 --sem-resposta
python workflow_triagem.py TCK-011 --sem-resposta
```

**O que apontar na tabela:** a coluna de chamadas é sempre 2; tempo e custo ficam na mesma faixa; a coluna gabarito compara com `tickets.json`. Em assinatura do Claude, o custo é estimativa do Claude Code, não cobrança por chamada.

### Slide 13 — Ato 2: agente (25 min)

| Tempo | O que fazer |
|---:|---|
| 3 min | Ler o pedido que o script envia (ele aparece no topo da saída) e as permissões: só `Read`, `Glob` e `Grep`, na pasta `dados`. |
| 7 min | Primeira execução do TCK-002 e leitura do resumo passo a passo. |
| 6 min | Segunda execução e comparação dos dois resumos em uma linha cada. |
| 5 min | Execução do TCK-011 com teto de US$ 0,05 para mostrar a parada por orçamento. |
| 4 min | Fechar o ato nomeando os conceitos: loop (2), variação (3), parada (4). |

```powershell
python rodar_agente.py --ticket TCK-002 --modo arquivos --saida a1-ato2-1.jsonl
(Get-Content a1-ato2-1.jsonl -Encoding UTF8 | Select-Object -Last 1 | ConvertFrom-Json).result
python rodar_agente.py --ticket TCK-002 --modo arquivos --saida a1-ato2-2.jsonl
python ler_execucao.py a1-ato2-1.jsonl --json
python ler_execucao.py a1-ato2-2.jsonl --json
python rodar_agente.py --ticket TCK-011 --modo arquivos --orcamento 0.05 --saida a1-ato2-teto.jsonl
```

O resumo corta a resposta final em 400 caracteres; a segunda linha mostra a resposta inteira, onde estão as recomendações ao time.

**O que apontar no resumo:** a ordem dos arquivos lidos; as voltas (`voltas`); o tempo total contra o tempo de API; o custo. Na segunda execução, o que mudou. Na execução com teto, o campo `subtype` do fim: o Claude Code registra a parada por orçamento (no SDK, `error_max_budget_usd`; conferir o nome exato no ensaio).

**Se o agente resolver o TCK-002 sem ler a política:** apontar a lacuna. A política diz que todo estorno gera nota e que acima de R$ 200 precisa de aprovação. Sem ler, ele recomendou bem por acaso, não por regra.

**Se o teto não cortar a execução do TCK-011:** baixar para `--orcamento 0.01`. O corte acontece depois da chamada que cruza o limite, então o gasto final pode passar um pouco do teto.

### Contingência

Sem rede ou sem Claude Code: abrir as saídas de `C:\demo\ensaio\` e dizer que são execuções reais do ensaio. O `ler_execucao.py` não chama o modelo, então mostra o registro do ensaio como se fosse ao vivo.

```powershell
Get-Content C:\demo\ensaio\ato1.txt
python ler_execucao.py C:\demo\ensaio\ato2-1.jsonl
python ler_execucao.py C:\demo\ensaio\ato2-teto.jsonl
```

Sem ensaio, abrir a seção Demonstração do guia interativo da aula, que traz execuções registradas por um modelo Claude, e dizer exatamente isso à turma: foram registradas antes, sem o Claude Code, com os arquivos colados no pedido.
"""

PLANO = {
    "formato": (
        "Cinco conceitos em cadeia, cada um consequência do anterior; uma demonstração em dois atos com o mesmo caso; "
        "20 minutos de apresentação de um monitor; uma discussão em que o professor apresenta os dois argumentos; e "
        "um fechamento que refaz o mapa. A turma não executa nada durante a aula: a prática está no estudo dirigido. "
        "Primeira aula do professor com a turma, por isso a abertura apresenta M3, M4, o formato e o caso Balcão."
    ),
    "objetivo": (
        "Diferenciar workflow de agente pelo critério de quem decide o próximo passo, explicar o custo da autonomia e "
        "a necessidade de uma política de parada, e aplicar uma regra de escolha a tipos de ticket do caso Balcão."
    ),
    "resultados": [
        "Explicar workflow como código que chama o modelo em passos fixos e reconhecer os cinco padrões de workflow.",
        "Explicar agente como loop em que o modelo escolhe a próxima ação e o resultado volta para a janela de contexto.",
        "Explicar por que autonomia aumenta custo, tempo e variação, e calcular o erro composto num exemplo.",
        "Escrever uma política de parada com objetivo verificável, tetos de passos, custo e tempo e condição de escalada.",
        "Decidir, para um tipo de problema, entre workflow e agente e justificar pela possibilidade de escrever os passos antes.",
    ],
    "ligacoes": ["retoma o pipeline de RAG do M2", "espelho do 1", "consequência do 2", "resposta ao 3", "síntese dos quatro"],
    "demo_resumo": "Mesmo caso nos dois atos: a fila de suporte do Balcão. Muda quem decide o próximo passo.",
    "atos": [
        ("Código fixa três passos", "Mostra o script, uma chamada isolada em JSON, roda três tickets e repete a classificação do TCK-011", "1 e 3"),
        ("Claude Code com leitura dos dados e teto de US$ 0,50", "Roda o TCK-002 duas vezes, compara os resumos e roda o TCK-011 com teto baixo", "2, 3 e 4"),
    ],
    "fechamento": [
        "**Monitor — 21h15–21h35, slide 14.** O caso Balcão em LangGraph: estado, nós e arestas; o workflow como grafo; o agente como grafo com volta e limite de recursão. Roteiro no guia do monitor.",
        "**Discussão — 21h35–21h48, slide 15.** O professor apresenta os dois argumentos (o agente investigou; o workflow repetiu e custou menos) e mostra que a decisão é por tipo de problema. Perguntas do chat entram se houver; a aula não depende delas.",
        "**Fechamento — 21h48–22h00, slide 16.** O mapa refeito e a resposta: dar autonomia quando o caminho se descobre no meio. O estudo dirigido é publicado no canal.",
    ],
    "riscos": [
        "Claude Code sem sessão: testar `claude -p` antes da aula; na falha, usar as saídas do ensaio ou o guia interativo.",
        "O agente pode demorar mais que o previsto: o roteiro do Ato 2 tem 4 minutos de folga no fechamento do ato.",
        "Rótulo do workflow divergente do gabarito: mostrar sem corrigir; é o gancho do M4.",
        "Custo exibido em assinatura é estimativa: dizer isso para não confundir com cobrança.",
    ],
}

ESTUDO = {
    "tempo": "cerca de 3 horas, em uma ou duas sentadas",
    "objetivo": (
        "Ao fim deste estudo você sabe dizer, para um problema concreto, se ele pede um workflow ou um agente, monta os "
        "dois no caso Balcão com o Claude Code e escreve a política de parada de um agente."
    ),
    "antes": [
        "Claude Code instalado e com login feito. Teste no terminal: `claude -p \"responda apenas: ok\"` precisa responder `ok`.",
        "Python 3.11 ou mais novo (`python --version`).",
        "A pasta `caso-balcao` do repositório da turma, [github.com/victorhwfreire/sistemas_ia_devs_b2c_20262](https://github.com/victorhwfreire/sistemas_ia_devs_b2c_20262), no seu computador. Os comandos abaixo partem de `caso-balcao/ferramentas`.",
        "No Windows PowerShell, rode antes `[Console]::OutputEncoding = [Text.Encoding]::UTF8` para os acentos saírem certos.",
    ],
    "conceitos": [
        {
            "titulo": "No workflow, o código decide o caminho",
            "definicao": "Workflow é código que chama o modelo em passos fixos: a ordem, os desvios e o fim estão escritos antes de rodar.",
            "texto": [
                "Um sistema com LLM raramente é uma chamada só. Na triagem do Balcão, uma chamada classifica o ticket, uma regra decide o time e outra chamada escreve a resposta. Quando a sequência é escrita no código, temos um workflow. O modelo trabalha dentro de cada passo; a passagem de um passo para o outro é do código.",
                "O RAG do M2 é um workflow: buscar trechos, montar o contexto, gerar a resposta, sempre nessa ordem. A Anthropic descreve cinco padrões que cobrem a maior parte dos workflows: encadeamento (a saída de uma chamada vira entrada da próxima), roteamento (uma classificação escolhe o caminho), paralelização (várias chamadas ao mesmo tempo, depois junta), orquestrador e trabalhadores (uma chamada divide a tarefa e outras executam) e avaliador e otimizador (uma chamada gera, outra critica e pede revisão).",
                "A vantagem do workflow é que ele é previsível. Dá para desenhar o fluxo antes de rodar, testar cada passo isolado, prever custo multiplicando chamadas por tickets e explicar depois por que algo aconteceu. A limitação é a mesma: ele só faz o que está escrito. Se o ticket pede uma investigação que não estava nos passos, ninguém investiga.",
            ],
            "fig": 6,
            "exemplo": "O `workflow_triagem.py` do caso faz duas chamadas ao modelo por ticket (classificar e responder) e uma decisão em código (o dicionário ROTA, que leva cada categoria a um time). Para doze tickets, são 24 chamadas, sempre.",
            "erro": "Achar que, por usar um LLM, o sistema é um agente. Se o caminho está no código, é workflow, mesmo que cada passo seja uma chamada sofisticada.",
            "pergunta": ("No workflow da triagem, qual passo não usa o modelo, e por que isso é bom?",
                         "O roteamento. Uma regra fixa por categoria é determinística, gratuita e testável; usar o modelo ali só traria custo e variação."),
        },
        {
            "titulo": "No agente, o modelo escolhe o próximo passo",
            "definicao": "Agente é um loop: o modelo olha o objetivo e o que já aconteceu, escolhe uma ação, recebe o resultado e decide de novo, até decidir parar.",
            "texto": [
                "No agente, você entrega ao modelo um objetivo e um conjunto de ferramentas, por exemplo ler arquivos ou consultar uma base. O modelo decide qual ação tomar. Seu código executa essa ação e devolve o resultado, que entra na janela de contexto. O modelo olha a janela, agora maior, e decide de novo. Em pseudocódigo: enquanto o modelo não disser que terminou, chame o modelo, execute o que ele pediu e devolva o resultado.",
                "Esse padrão foi descrito em 2022 no artigo ReAct, que alterna raciocinar e agir. O Claude Code que você usa é um agente desse tipo: um modelo num loop com ferramentas para ler, editar e rodar comandos. Quando você pede uma mudança no código, ele decide sozinho quais arquivos abrir, o que testar e quando parar.",
                "O modelo do agente é o mesmo do workflow. O que muda é quem decide a próxima ação. E decidir a próxima ação inclui decidir quantas ações tomar: é daí que vêm a flexibilidade e o custo do agente.",
            ],
            "fig": 7,
            "exemplo": "Com o objetivo “resolva o TCK-002” e permissão só de leitura na pasta `dados`, o agente das execuções registradas para o guia listou a pasta, leu a política, os clientes e as cobranças de uma vez, achou dois lançamentos de R$ 189,90 em 05/10 (COB-5002 e COB-5003) e recomendou estornar o COB-5003. Sem o pedido mandar, também apontou a mesma duplicidade no Bazar Estrela.",
            "erro": "Chamar de agente qualquer chatbot. Um chat que só responde, sem ferramentas e sem loop de ação, é uma chamada ao modelo, não um agente.",
            "pergunta": ("Por que o resultado de cada ferramenta precisa voltar para a janela de contexto?",
                         "Porque o modelo só decide com o que está na janela. Se o resultado não volta, a próxima decisão é tomada às cegas."),
        },
        {
            "titulo": "Cada passo a mais é uma chance a mais de errar",
            "definicao": "Autonomia custa tempo, dinheiro e risco: o número de passos vira variável e o erro de cada passo se acumula.",
            "texto": [
                "Cada volta do agente é mais uma chamada ao modelo. Ela custa tempo, porque espera a resposta; custa dinheiro, porque reenvia a janela inteira, que cresce a cada volta; e custa risco, porque cada decisão pode estar errada.",
                "O risco se acumula. Se cada passo acerta 95% das vezes e os passos fossem independentes, uma execução de 5 passos acertaria 0,95⁵ ≈ 77%; de 10 passos, 0,95¹⁰ ≈ 60%; de 20 passos, 0,95²⁰ ≈ 36%. Na prática os passos não são independentes, e o agente às vezes corrige um erro anterior, mas a direção vale: cadeias longas erram mais.",
                "O segundo efeito é a variação. O mesmo ticket, rodado duas vezes, pode levar três passos numa execução e seis na outra. Custo e tempo passam a ter uma faixa, não um valor. No workflow, o número de chamadas por ticket é fixo.",
            ],
            "fig": 8,
            "exemplo": "Nas duas execuções registradas do TCK-002, o agente seguiu o mesmo caminho, mas escreveu respostas diferentes ao cliente: uma disse que o estorno “está aprovado”, a outra, “vamos estornar”. Com mais dados e mais ferramentas, o caminho também varia. Compare os seus resumos com `ler_execucao.py --json`.",
            "erro": "Medir um agente com uma execução só. Uma execução boa não diz quanto ele custa nem quantas vezes acerta; isso é tema do M4.",
            "pergunta": ("Com 90% de acerto por passo, quanto acerta uma execução de 10 passos independentes?",
                         "0,9¹⁰ ≈ 35%. Um pouco mais de uma em cada três execuções."),
        },
        {
            "titulo": "Todo agente precisa de uma política de parada",
            "definicao": "Política de parada é a regra, escrita antes de rodar, de quando o loop termina: objetivo cumprido, limite atingido ou passagem para uma pessoa.",
            "texto": [
                "Se cada volta custa e arrisca, alguém precisa decidir quando o loop acaba, e não pode ser só o modelo. A política de parada tem cinco campos: objetivo verificável (como sei que terminou), teto de passos, teto de custo, teto de tempo e condição de escalada para uma pessoa.",
                "A condição de escalada cobre dois casos. Falta de progresso: duas voltas sem informação nova na janela é sinal de que o agente está andando em círculo. Ação sensível: um estorno, uma exclusão, um e-mail para o cliente. Nesses casos, o agente para e passa o caso adiante com o que já descobriu.",
                "No Claude Code em modo não interativo (`claude -p`), `--max-budget-usd` limita o gasto estimado e `--max-turns` limita as voltas. O corte acontece depois da chamada que cruzou o limite, então o gasto final pode passar um pouco do teto. A política não deixa o agente mais inteligente; ela garante que o erro tem tamanho máximo.",
            ],
            "fig": 9,
            "exemplo": "Política do agente de cobrança do Balcão: objetivo = recomendação com o id do lançamento conferido; até 8 voltas; até US$ 0,50; até 2 minutos; escala para o financeiro se o estorno passar de R$ 200 ou se duas voltas seguidas não trouxerem dado novo.",
            "erro": "Confiar que o modelo vai parar quando terminar. Em geral ele para, mas a política existe para os casos em que não para.",
            "pergunta": ("Qual campo da política impede que um agente fique relendo o mesmo arquivo por dez voltas?",
                         "A condição de falta de progresso, reforçada pelo teto de passos."),
        },
        {
            "titulo": "Comece pelo workflow; suba para agente com motivo",
            "definicao": "Se dá para escrever os passos antes, é workflow. Se o caminho depende do que se descobre no meio, é agente, com limites.",
            "texto": [
                "A pergunta que decide é: dá para escrever os passos antes de rodar? Para uma dúvida de produto, dá: classificar, responder com o artigo certo, fim. Para uma cobrança contestada, o caminho depende do que aparece: é duplicidade, tarifa sem contrato, antecipação contratada? Escrever todos esses desvios antes é caro e frágil; o agente se paga.",
                "Os dois se combinam. Um desenho comum é o workflow que roteia e chama um agente só na categoria que precisa investigar. Assim o custo e a variação do agente ficam restritos aos tickets que ganham com eles.",
                "A recomendação da Anthropic, no texto de 2024, é começar pela solução mais simples que resolve e só acrescentar autonomia quando houver ganho medido. Muita equipe faz o contrário: começa pelo agente porque impressiona na demonstração e descobre o custo em produção.",
            ],
            "fig": 10,
            "exemplo": "No Balcão: `duvida_produto` e `falha_transacao` com passos conhecidos vão por workflow; `cobranca_indevida`, que exige conferir lançamentos e contrato, vai para o agente com teto de US$ 0,50 e escalada acima de R$ 200.",
            "erro": "Tratar agente como upgrade natural de workflow. É outra decisão de projeto, com outro custo.",
            "pergunta": ("Um sistema que sempre extrai os mesmos cinco campos de uma nota fiscal pede workflow ou agente?",
                         "Workflow. Os passos são conhecidos antes; um agente só traria variação."),
        },
    ],
    "glossario": [
        ("Workflow", "código que chama o modelo em passos fixos."),
        ("Agente", "loop em que o modelo escolhe a próxima ação até decidir parar."),
        ("Ferramenta (tool)", "função que o modelo pode pedir para executar: ler, consultar, gravar."),
        ("Janela de contexto", "tudo o que o modelo recebe numa chamada; no agente, cresce a cada volta."),
        ("Encadeamento", "padrão em que a saída de uma chamada vira entrada da próxima."),
        ("Roteamento", "padrão em que uma classificação escolhe o caminho seguinte."),
        ("Saída estruturada", "resposta forçada a seguir um esquema JSON; no Claude Code, `--json-schema`."),
        ("Erro composto", "queda do acerto total quando vários passos com erro se encadeiam."),
        ("Política de parada", "regra escrita de quando o loop termina."),
        ("Escalada", "passagem do caso para uma pessoa, com o que o agente já descobriu."),
        ("`claude -p`", "Claude Code em modo não interativo: recebe o pedido, executa e devolve o resultado."),
        ("`--output-format json` e `stream-json`", "saída com resultado, tempo e custo; o segundo traz cada passo da execução."),
    ],
    "praticas": [
        {
            "titulo": "Prática 1 · Monte o workflow de triagem",
            "tempo": "50 min",
            "objetivo": "Construir, com o Claude Code, um workflow de três passos para os tickets do Balcão e medir chamadas, tempo e custo.",
            "passos": [
                {"t": "Abra um terminal na pasta `caso-balcao` e faça uma chamada isolada ao modelo, pedindo JSON.",
                 "cmd": "claude -p \"Classifique este ticket em uma palavra: maquininha não passa débito desde as 9h.\" --output-format json"},
                {"t": "Leia o JSON devolvido e localize `result` (a resposta), `duration_ms` (o tempo) e `total_cost_usd` (o custo estimado). Em assinatura, o custo é estimativa, não cobrança."},
                {"t": "Abra o Claude Code na pasta (`claude`) e peça o script, com este texto:",
                 "prompt": "Crie meu_workflow.py em ferramentas/. Para cada ticket de tickets.json, faça três passos: (1) chame `claude -p` com --output-format json e --json-schema para obter categoria (uma das categorias de tickets.json) e prioridade (P1, P2 ou P3), usando a política de dados/politica-atendimento.md como instrução; (2) escolha o time com um dicionário Python, sem modelo; (3) chame `claude -p` de novo para redigir uma resposta de três frases ao cliente. Mande o pedido pela entrada padrão. Imprima uma tabela com ticket, categoria, prioridade, time, tempo e custo, e compare categoria e prioridade com o gabarito."},
                {"t": "Antes de aceitar, leia o código que ele propôs e confira: o roteamento está em código? O pedido vai pela entrada padrão? Depois rode em três tickets.",
                 "cmd": "python ferramentas/meu_workflow.py TCK-001 TCK-002 TCK-011"},
                {"t": "Compare com a versão de referência do caso, que faz o mesmo.",
                 "cmd": "python ferramentas/workflow_triagem.py TCK-001 TCK-002 TCK-011"},
            ],
            "observe": [
                "O número de chamadas por ticket é sempre o mesmo.",
                "Tempo e custo ficam numa faixa estreita de um ticket para o outro.",
                "O TCK-011 (a farmácia) é classificado, mas ninguém investiga se foi tarifa ou erro.",
            ],
            "pronto": "O seu script roda nos doze tickets e imprime a tabela com acerto contra o gabarito.",
            "extra": "Troque o modelo com `--model haiku` nas chamadas e compare tempo, custo e acerto.",
        },
        {
            "titulo": "Prática 2 · Rode o mesmo ticket como agente e compare",
            "tempo": "45 min",
            "objetivo": "Ver o loop do agente num registro de execução e medir a variação entre execuções do mesmo pedido.",
            "passos": [
                {"t": "Rode o agente no TCK-002, com leitura liberada só na pasta `dados` e teto de US$ 0,50.",
                 "cmd": "cd ferramentas\npython rodar_agente.py --ticket TCK-002 --modo arquivos --saida ag1.jsonl"},
                {"t": "Leia o resumo: quais arquivos ele leu, em que ordem, quantas voltas, quanto tempo e quanto custou."},
                {"t": "Rode de novo, duas vezes, gravando em arquivos diferentes.",
                 "cmd": "python rodar_agente.py --ticket TCK-002 --modo arquivos --saida ag2.jsonl\npython rodar_agente.py --ticket TCK-002 --modo arquivos --saida ag3.jsonl"},
                {"t": "Compare as três execuções em uma linha cada.",
                 "cmd": "python ler_execucao.py ag1.jsonl --json\npython ler_execucao.py ag2.jsonl --json\npython ler_execucao.py ag3.jsonl --json"},
                {"t": "Agora rode o TCK-004, uma dúvida simples, como agente e como workflow, e compare custo e tempo.",
                 "cmd": "python rodar_agente.py --ticket TCK-004 --modo arquivos --saida ag-duvida.jsonl\npython workflow_triagem.py TCK-004"},
                {"t": "Abra `ag1.jsonl` num editor e encontre um bloco `tool_use` e o `tool_result` correspondente: é o formato do loop que a aula 2 vai explicar."},
            ],
            "observe": [
                "O agente decide o que ler; o pedido não diz quais arquivos abrir.",
                "Entre as três execuções do TCK-002, compare voltas, tempo, custo e o texto da resposta: o que variou e o que se repetiu?",
                "Para a dúvida simples, o agente custa mais e não entrega mais que o workflow.",
            ],
            "pronto": "Você preencheu uma tabela com voltas, arquivos lidos, tempo e custo das três execuções e escreveu em uma frase quando o agente compensou.",
            "extra": "Faça o agente ler um arquivo que não está liberado (peça no `--pedido` para editar a política) e encontre a negação no registro.",
        },
        {
            "titulo": "Prática 3 · Escreva a política de parada de um agente seu",
            "tempo": "35 min",
            "objetivo": "Transformar a política de parada em texto concreto para um agente do seu contexto de trabalho e testar um teto.",
            "passos": [
                {"t": "Escolha uma tarefa do seu trabalho que você daria a um agente. Escreva em um parágrafo o objetivo e as ferramentas que ele teria."},
                {"t": "Preencha os cinco campos: objetivo verificável; teto de passos; teto de custo; teto de tempo; condição de escalada (falta de progresso e ação sensível)."},
                {"t": "Peça ao Claude uma crítica da sua política, com este texto (troque os colchetes):",
                 "prompt": "Sou dev e vou colocar um agente em produção. Tarefa: [descreva]. Ferramentas: [liste]. Política de parada: [cole os cinco campos]. Aponte, em no máximo cinco itens, situações em que essa política deixaria o agente rodar demais ou parar cedo demais, e sugira um ajuste para cada uma."},
                {"t": "Teste um teto de verdade no caso Balcão: rode o TCK-011 com orçamento muito baixo e veja como a execução termina.",
                 "cmd": "python rodar_agente.py --ticket TCK-011 --modo arquivos --orcamento 0.01 --saida teto.jsonl"},
                {"t": "No resumo, confira o campo de fim (`subtype`) e o custo final. Ele passou do teto? Explique por quê em uma frase."},
            ],
            "observe": [
                "O corte acontece depois da chamada que cruza o limite.",
                "Uma política sem condição de escalada só sabe parar, não sabe para quem passar o caso.",
            ],
            "pronto": "Você tem a política de parada em cinco campos, revisada com a crítica do Claude, e entende como o teto de orçamento termina uma execução.",
            "extra": "Desenhe o híbrido do Balcão: workflow para todas as categorias e agente só para `cobranca_indevida`. Quanto custaria o lote de doze tickets nesse desenho?",
        },
    ],
    "autoavaliacao": [
        "Consigo dizer, olhando um sistema, quem decide o próximo passo: o código ou o modelo.",
        "Consigo citar três dos cinco padrões de workflow e um exemplo de cada no Balcão.",
        "Consigo explicar o loop do agente e por que o resultado da ferramenta volta para a janela.",
        "Consigo calcular o erro composto de uma cadeia de passos e dizer por que é só uma aproximação.",
        "Consigo escrever os cinco campos de uma política de parada.",
        "Consigo justificar workflow ou agente para um tipo de problema com a pergunta “dá para escrever os passos antes?”.",
    ],
    "leituras": [
        ("Anthropic, “Building effective agents” (19/12/2024)", "https://www.anthropic.com/engineering/building-effective-agents",
         "definições de workflow e agente e os cinco padrões"),
        ("Yao et al., “ReAct: Synergizing Reasoning and Acting in Language Models” (ICLR 2023)", "https://arxiv.org/abs/2210.03629",
         "o artigo que descreveu o loop de raciocinar e agir"),
        ("Claude Code, modo não interativo (headless)", "https://code.claude.com/docs/en/headless",
         "`claude -p`, formatos de saída e saída estruturada"),
        ("Claude Code, referência da CLI", "https://code.claude.com/docs/en/cli-reference",
         "opções como --max-budget-usd, --max-turns e --allowedTools"),
    ],
}

MONITOR = {
    "resumo": (
        "Primeira aula do professor com a turma. Apresenta M3 e M4, o formato (aula expositiva, monitor, estudo dirigido) "
        "e o caso Balcão. O conteúdo é a diferença entre workflow e agente, o custo da autonomia e a política de parada, "
        "demonstrada com um script de triagem e com o Claude Code agindo nos dados do caso."
    ),
    "termos": [
        ("Workflow", "código que chama o modelo em passos fixos; o caminho é do código."),
        ("Agente", "loop em que o modelo escolhe a próxima ação; o caminho é do modelo."),
        ("Cinco padrões de workflow", "encadeamento, roteamento, paralelização, orquestrador e trabalhadores, avaliador e otimizador."),
        ("ReAct", "padrão de 2022 que alterna raciocinar e agir; base dos agentes atuais."),
        ("Erro composto", "0,95 elevado ao número de passos: cadeias longas erram mais."),
        ("Política de parada", "objetivo verificável, tetos de passos, custo e tempo, condição de escalada."),
        ("`claude -p`", "Claude Code sem interação; com `--output-format json` devolve resultado, tempo e custo."),
        ("`--json-schema`", "força a resposta a seguir um esquema; o objeto sai em `structured_output`."),
        ("`--max-budget-usd`", "teto de gasto estimado de uma execução em modo -p."),
        ("`stream-json`", "registro passo a passo da execução: cada `tool_use` e cada `tool_result`."),
    ],
    "antes": [
        "Ler o roteiro (Parte 1 inteira e Parte 2 da demonstração) e o estudo dirigido da aula.",
        "Testar o próprio Claude Code com `claude -p \"responda apenas: ok\"`; se falhar, `claude` e `/login`.",
        "Rodar uma vez `python workflow_triagem.py TCK-002` e `python rodar_agente.py --ticket TCK-002 --modo arquivos` na pasta `caso-balcao/ferramentas`, para reconhecer a saída na tela do professor.",
        "Abrir e deixar à mão: o guia interativo da aula (seção Demonstração), o PDF do estudo dirigido e o repositório da turma, com o caso Balcão e os estudos dirigidos: [github.com/victorhwfreire/sistemas_ia_devs_b2c_20262](https://github.com/victorhwfreire/sistemas_ia_devs_b2c_20262).",
        "Combinar com o professor o sinal no chat privado para tempo (“5 min”) e para pergunta pendente (“P?”).",
        "Ensaiar a apresentação de 20 minutos com cronômetro.",
    ],
    "durante": {
        "Abertura": "Publicar no chat, às 19h, os links do guia interativo e do repositório da turma, [github.com/victorhwfreire/sistemas_ia_devs_b2c_20262](https://github.com/victorhwfreire/sistemas_ia_devs_b2c_20262). Responder dúvidas de acesso em privado.",
        "Mapa da aula": "Nada a fazer além de acompanhar o chat. Se alguém perguntar sobre nota ou presença, responder que é com a coordenação.",
        "Conceitos": "Separar perguntas de conteúdo num bloco de notas, com o nome de quem perguntou. Dúvidas de configuração (Claude Code, Python) são respondidas por você no chat. Ao fim de cada conceito, mandar no privado do professor “P?” se houver pergunta boa.",
        "Intervalo": "Avisar no chat que a volta é às 20h25. Revisar as perguntas separadas e escolher até três para a discussão.",
        "Demonstração": "Ficar com o guia interativo aberto na seção Demonstração: se o Claude Code do professor falhar, enviar o link no chat. Avisar no privado se a fonte do terminal estiver ilegível.",
        "Monitor": "Apresentar os 20 minutos. O professor cronometra e avisa aos 17.",
        "Discussão": "Ler para o professor até três perguntas do chat, em voz alta, já resumidas em uma frase.",
        "Fechamento": "Publicar o PDF do estudo dirigido e o guia interativo no canal da turma. Agradecer e lembrar a data da próxima aula.",
    },
    "atencao": [
        "Workflow que usa LLM continua sendo workflow. A confusão mais comum é chamar qualquer coisa com LLM de agente.",
        "A tabela de erro composto é ilustrativa (passos independentes, 95% cada). Não apresentar como dado de benchmark.",
        "O custo que o Claude Code mostra em assinatura é estimativa; ninguém é cobrado por chamada.",
        "Não antecipar o formato do tool use nem o MCP: são das aulas 2 e 3. Se perguntarem, “o professor abre isso segunda”.",
        "A turma não é obrigada a falar. Não chamar ninguém pelo nome nem pedir câmera.",
    ],
    "contribuir": [
        "Trazer, no chat, um exemplo de mercado de cada lado: um workflow (pipeline de RAG, automação no n8n) e um agente (Claude Code, modo agente de IDEs).",
        "Responder dúvidas de instalação com o trecho exato do estudo dirigido.",
        "Anotar as três dúvidas mais frequentes para o FAQ da aula, publicado no canal no dia seguinte.",
        "No seu tema de 20 minutos, usar o caso Balcão: a turma acompanha melhor quando o exemplo é o mesmo.",
    ],
    "duvidas": [
        ("O Claude Code é um agente ou um workflow?", "Agente: o modelo decide quais ferramentas usar e quando parar. O `workflow_triagem.py` usa o Claude Code como chamada isolada, sem ferramentas, dentro de um workflow."),
        ("Preciso de chave de API para as práticas?", "Não. Tudo roda com o login do Claude Code. O custo exibido é estimativa."),
        ("LangGraph é obrigatório?", "Não. É o tema da apresentação do monitor; o curso usa Python puro e o Claude Code."),
        ("O que acontece quando o teto de orçamento estoura?", "A execução para depois da chamada que cruzou o limite e registra o motivo no fim do JSON."),
        ("Agente sempre acerta mais?", "Não. Ele investiga mais, mas varia mais e custa mais. Para tarefas de passos conhecidos, workflow costuma acertar igual por menos."),
    ],
    "apresentacao": {
        "titulo": "O caso Balcão em LangGraph: workflow e agente como grafo de estados",
        "porque": "A aula mostra workflow e agente com Python puro e com o Claude Code. O LangGraph é o framework mais usado no ecossistema Python para os dois desenhos e está na stack de referência do curso; ver o mesmo caso como grafo fixa os conceitos.",
        "roteiro": [
            ("5 min", "Vocabulário do grafo", "Estado (um dicionário tipado que passa de nó em nó), nós (funções) e arestas (fixas ou condicionais). Um desenho na tela, sem código ainda."),
            ("5 min", "O workflow da triagem como grafo", "Nó classificar → aresta condicional por categoria → nó responder. Mostrar que a aresta condicional faz o papel do dicionário ROTA."),
            ("6 min", "O agente como grafo com volta", "Nó do modelo ↔ nó das ferramentas, com a aresta que volta enquanto houver chamada de ferramenta. O `recursion_limit` como teto de passos, ligando à política de parada da aula."),
            ("4 min", "Quando o framework compensa", "Checkpoint do estado, interrupção para aprovação humana e visualização do grafo, contra o custo de mais uma dependência. Fechar com uma frase: o framework não decide se é workflow ou agente; o desenho decide."),
        ],
        "fontes": [
            "Documentação do LangGraph (seções de workflows e agentes, e de limite de recursão).",
            "Anthropic, “Building effective agents” (2024), para manter o mesmo vocabulário da aula.",
        ],
        "evitar": [
            "Redefinir workflow e agente: o professor acabou de fazer isso; partir das definições dele.",
            "Codar ao vivo do zero. Levar o código pronto e mostrar por partes.",
            "Comparar frameworks em tabela longa. O foco é o caso Balcão como grafo.",
        ],
        "alternativa": "Os cinco padrões de workflow da Anthropic com um exemplo real de cada (pipeline de RAG, roteador de atendimento, revisão em paralelo, orquestrador de tarefas, gerador com revisor).",
    },
    "depois": [
        "Publicar no canal, no dia seguinte, o FAQ com as três dúvidas mais frequentes.",
        "Responder no canal, até a próxima aula, dúvidas das práticas do estudo dirigido.",
        "Mandar ao professor, em duas linhas, o que funcionou e o que travou na sua apresentação.",
    ],
}
