"""Conteúdo do guia interativo da aula 1 do M3: workflow ou agente."""
from html import escape as e


def voltas_html(item):
    linhas = "".join(f'<div class="volta"><small>Volta {k}</small><span>{" · ".join(f"<code>{e(c)}</code>" for c in chamadas)}</span></div>'
                     for k, chamadas in enumerate(item["voltas"], 1))
    final = len(item["voltas"]) + 1
    return f'<div class="voltas">{linhas}<div class="volta"><small>Volta {final}</small><span>Nenhuma ferramenta: o modelo decide parar e escreve a resposta.</span></div></div>'


def construir(ctx):
    ag1, ag2 = ctx.reg("m3a1-agente-TCK-002", 1), ctx.reg("m3a1-agente-TCK-002", 2)
    ticket = ("<p><b>TCK-002 · Estúdio Pilates Vida</b></p><p>“Fui cobrada duas vezes da mensalidade do plano Pro em outubro. "
              "O extrato mostra dois lançamentos de R$ 189,90 no dia 05/10. Quero o estorno de um deles.”</p>")
    return {
        "title": "Workflow ou agente",
        "pergunta": "Quando vale dar autonomia ao modelo?",
        "h1": 'Dê <span class="mais">autonomia</span> ao modelo quando o caminho se descobre no meio',
        "lide": ("Esta página acompanha a aula 1 do M3. São cinco ideias em cadeia, cada uma consequência da anterior. "
                 "Cada uma aparece acontecendo: numa bancada para mexer e em execuções reais de um modelo Claude no caso Balcão."),
        "carimbo": "claude-opus-5-5, uma conversa nova por execução, em 10/11/2026",
        "partida": {
            "h2": "Antes de começar: três termos e um caso",
            "ambiente": [
                ("Chamada ao modelo", "Você manda um texto e recebe um texto. No curso, quem faz a chamada é o Claude Code em modo não interativo, "
                 "<code>claude -p</code>, que devolve a resposta em JSON com tempo e custo."),
                ("Ferramenta", "Uma função que o modelo pode pedir para executar: ler um arquivo, consultar um cadastro. Quem executa é o seu "
                 "código. A aula 2 abre essa caixa."),
                ("Caso Balcão", "Plataforma fictícia de pagamentos para pequenos comércios. O suporte recebe tickets em texto livre e precisa "
                 "triar, investigar e responder. O ticket de hoje está ao lado."),
            ],
            "historia": (
                f"<h3>O ticket de hoje e o que os dados dizem</h3>{ticket}"
                "<ul><li><b>cobrancas.json</b> tem, para o cliente CLI-102, os lançamentos <code>COB-5002</code> e <code>COB-5003</code>: "
                "os dois em 05/10/2026, tipo mensalidade, R$ 189,90, pagos.</li>"
                "<li><b>politica-atendimento.md</b>: estorno só para cobrança duplicada ou tarifa sem contrato comprovada; no valor do lançamento; "
                "até R$ 200,00 o atendimento emite, acima disso precisa de aprovação do financeiro; todo estorno gera nota.</li></ul>"
            ),
        },
        "conceitos": [
            {
                "nav": "Workflow", "tema": "Workflow", "fio": "o código decide o caminho", "slide": 6,
                "h2": "No workflow, o código decide o caminho",
                "definicao": "Workflow é código que chama o modelo em passos fixos: a ordem, os desvios e o fim estão escritos antes de rodar.",
                "prosa": [
                    "O RAG do M2 já era um workflow: buscar trechos, montar o contexto, gerar a resposta, sempre nessa ordem. Na triagem do Balcão, "
                    "uma chamada classifica o ticket, uma linha de código escolhe o time e outra chamada escreve a resposta.",
                    "O modelo trabalha dentro de cada caixa; a seta entre as caixas é do código. Por isso dá para testar cada passo, prever o custo e "
                    "explicar depois o que aconteceu.",
                ],
                "bancada": {
                    "tipo": "passos", "real": True, "selo": "Execução registrada",
                    "h3": "O workflow da triagem, passo a passo, no TCK-002",
                    "p": "Avance um passo de cada vez. As duas chamadas ao modelo são execuções reais; o roteamento é uma linha de Python.",
                    "passos": [
                        {"t": "Entrada", "e": "O ticket entra como texto. O workflow não olha os dados do Balcão: só o texto do cliente.", "c": ticket},
                        {"t": "Passo 1 · Classificar (modelo)",
                         "e": "Uma chamada ao modelo, com a política como instrução. No script, a saída é forçada por <code>--json-schema</code>; aqui, o formato foi pedido no texto.",
                         "c": {"lista": [ctx.pedido("m3a1-clas-TCK-002"), ctx.saida("m3a1-clas-TCK-002")]}},
                        {"t": "Passo 2 · Rotear (código)",
                         "e": "Nenhuma chamada ao modelo. Um dicionário do Python leva a categoria ao time: determinístico, gratuito e testável.",
                         "c": '<pre class="cmd">ROTA = {"falha_transacao": "pagamentos", "cobranca_indevida": "financeiro", ...}\ntime_destino = ROTA["cobranca_indevida"]   # financeiro</pre>'},
                        {"t": "Passo 3 · Responder (modelo)",
                         "e": "A segunda chamada ao modelo escreve a primeira resposta ao cliente, sem prometer estorno nem prazo.",
                         "c": {"lista": [ctx.pedido("m3a1-resp-TCK-002"), ctx.saida("m3a1-resp-TCK-002")]}},
                        {"t": "O que isso mostra",
                         "e": "<b>Duas chamadas ao modelo e uma decisão em código, para qualquer ticket.</b> A resposta está correta e cordial, mas ninguém "
                              "conferiu os lançamentos: investigar não estava entre os passos."},
                    ],
                    "vivo": "m3a1-clas-TCK-002", "vivo_rotulo": "Rodar a classificação agora",
                },
                "pratica": "Antes de chamar o modelo num passo, pergunte se uma regra de código resolve. Roteamento, formatação e validação raramente precisam de LLM.",
                "pergunta": ("o workflow da triagem resolveria o TCK-002 sozinho?",
                             "Classificaria e responderia bem, como mostra o passo 3. Mas não confirmaria a duplicidade nem diria qual lançamento estornar: "
                             "esse passo não está escrito. Ou alguém acrescenta um passo fixo de consulta, ou o caso vai para um agente."),
            },
            {
                "nav": "Agente", "tema": "Agente", "fio": "o modelo decide o próximo passo", "slide": 7,
                "h2": "No agente, o modelo escolhe o próximo passo",
                "definicao": "Agente é um loop: o modelo olha o objetivo e o que já aconteceu, escolhe uma ação, recebe o resultado e decide de novo, até decidir parar.",
                "prosa": [
                    "Segundo conceito, o espelho do primeiro. Agora o pedido traz só o objetivo, resolver o TCK-002, e as ferramentas: listar e ler "
                    "arquivos da pasta de dados. O modelo decide o que fazer; o resultado de cada ferramenta volta para a janela de contexto, e ele decide de novo.",
                    "O Claude Code que você usa é um agente desses. O modelo é o mesmo do workflow; muda quem segura o volante.",
                ],
                "bancada": {
                    "tipo": "passos", "real": True, "selo": "Execução registrada",
                    "h3": "O agente no TCK-002: as voltas de uma execução real",
                    "p": "Um subagente do Claude Code recebeu o pedido e só as ferramentas de leitura, numa cópia da pasta de dados. Estas foram as voltas dele.",
                    "passos": [
                        {"t": "O pedido", "e": "O pedido diz o objetivo e o formato do fim, mas não diz quais arquivos abrir.",
                         "c": ctx.pedido("m3a1-agente-TCK-002")},
                        {"t": "As voltas", "e": "Na primeira volta, o modelo listou a pasta. Na segunda, pediu os três arquivos de uma vez, em paralelo. Na terceira, "
                                               "sem nova ferramenta, decidiu parar e escrever. Ninguém escreveu esses passos.",
                         "c": voltas_html(ag1)},
                        {"t": "A resposta", "e": "A resposta registrada, sem edição. Repare no item 4: o agente achou a mesma duplicidade no Bazar Estrela, que o pedido não mencionava.",
                         "c": ctx.saida("m3a1-agente-TCK-002", 1)},
                        {"t": "O que isso mostra",
                         "e": "<b>O agente investigou o que o workflow não investigava</b>: confirmou o lançamento COB-5003, conferiu a regra dos R$ 200 e "
                              "foi além do ticket. O preço é que o caminho e o custo deixam de ser decididos por você."},
                    ],
                },
                "pratica": "Dê ao agente só as ferramentas de que ele precisa. Aqui, leitura bastou; a permissão de editar teria sido risco sem ganho.",
                "pergunta": ("por que o resultado de cada ferramenta precisa voltar para a janela?",
                             "Porque o modelo só decide com o que está na janela. Sem o conteúdo de cobrancas.json na janela, a próxima decisão seria um palpite."),
            },
            {
                "nav": "Custo", "tema": "Custo da autonomia", "fio": "cada passo é chance de errar", "slide": 8,
                "h2": "Cada passo a mais é uma chance a mais de errar",
                "definicao": "Autonomia custa tempo, dinheiro e risco: o número de passos vira variável e o erro de cada passo se acumula.",
                "prosa": [
                    "Terceiro conceito, consequência do segundo. Se o modelo decide quantas voltas dar, cada volta cobra tempo, custo (a janela inteira é reenviada) e uma nova chance de erro.",
                    "Mexa na bancada: com 95% de acerto por passo, dez passos independentes acertam cerca de 60%. É uma aproximação, porque os passos reais não são "
                    "independentes e o agente às vezes corrige um erro anterior, mas a direção vale.",
                ],
                "bancada": {
                    "tipo": "composto", "h3": "Erro composto",
                    "p": "Escolha o acerto de cada passo e o número de passos em sequência. A barra mostra o acerto da execução inteira.",
                    "aviso": "Valores ilustrativos: o cálculo supõe passos independentes, cada um com o mesmo acerto.",
                    "marcos": [1, 5, 10, 20, 30],
                },
                "pratica": "Desconfie de agentes que precisam de dezenas de passos para tarefas simples. Encurtar o caminho costuma melhorar mais que trocar de modelo.",
                "pergunta": ("nas execuções registradas, o caminho do agente variou?",
                             "Não. Nas duas, o agente listou a pasta e leu os três arquivos de uma vez. A variação apareceu no texto: uma resposta disse que o estorno "
                             "“está aprovado”, a outra, “vamos estornar”. Com poucos dados o caminho tende a se repetir; com mais dados e ferramentas, também varia."),
            },
            {
                "nav": "Parada", "tema": "Política de parada", "fio": "limite escrito antes de rodar", "slide": 9,
                "h2": "Todo agente precisa de uma política de parada",
                "definicao": "Política de parada é a regra, escrita antes de rodar, de quando o loop termina: objetivo cumprido, limite atingido ou passagem para uma pessoa.",
                "prosa": [
                    "Quarto conceito, a resposta de engenharia ao terceiro. Cinco campos: objetivo verificável, teto de passos, teto de custo, teto de tempo e "
                    "condição de passar para uma pessoa (falta de progresso ou ação sensível).",
                    "No Claude Code sem interação, <code>--max-budget-usd</code> e <code>--max-turns</code> limitam a execução. A política não deixa o agente mais esperto; "
                    "ela limita o tamanho do erro.",
                ],
                "bancada": {
                    "tipo": "quiz", "h3": "O que a política manda fazer?",
                    "p": "Situações ao fim de uma volta de um agente de cobrança do Balcão, com teto de US$ 0,50. Escolha a decisão.",
                    "chave_html": "Objetivo: recomendação com o id do lançamento conferido. Escalada: estorno acima de R$ 200 ou duas voltas sem dado novo.",
                    "aviso": "Situações ilustrativas, montadas a partir do caso.",
                    "opcoes": [["c", "Continua"], ["e", "Para e entrega"], ["p", "Para e passa a uma pessoa"]],
                    "itens": [
                        {"origem": "Volta 2", "t": "Leu cobrancas.json e achou os dois lançamentos, mas ainda não leu a política de estorno.", "r": "c",
                         "fb": "Falta o dado que decide o estorno. Houve progresso e nenhum limite estourou: mais uma volta."},
                        {"origem": "Volta 3", "t": "Leu a política, conferiu o COB-5003 de R$ 189,90 e escreveu a recomendação.", "r": "e",
                         "fb": "O objetivo verificável foi cumprido: recomendação com o id do lançamento conferido."},
                        {"origem": "Volta 6", "t": "As duas últimas voltas releram o mesmo arquivo, sem nenhum dado novo.", "r": "p",
                         "fb": "Falta de progresso é condição de escalada: para e passa adiante o que já descobriu."},
                        {"origem": "Volta 3", "t": "O agente quer recomendar um estorno de R$ 489,00 da mensalidade da TechParts.", "r": "p",
                         "fb": "Acima de R$ 200 a política exige aprovação do financeiro: ação sensível vai para uma pessoa."},
                        {"origem": "Volta 5", "t": "O gasto estimado chegou a US$ 0,52, com teto de US$ 0,50, e ainda não há resposta.", "r": "p",
                         "fb": "Teto de custo atingido: a execução para. Sem resposta, o que foi descoberto vai para uma pessoa."},
                    ],
                },
                "pratica": "Escreva a política antes de rodar o primeiro agente em produção, e registre qual campo encerrou cada execução.",
                "pergunta": ("o teto de orçamento garante gasto menor que o teto?",
                             "Não exatamente. O corte acontece depois da chamada que cruzou o limite, então o gasto final pode passar um pouco do valor."),
            },
            {
                "nav": "Escolha", "tema": "Síntese", "fio": "workflow primeiro, agente com motivo", "slide": 10,
                "h2": "Comece pelo workflow; suba para agente com motivo",
                "definicao": "Se dá para escrever os passos antes, é workflow. Se o caminho depende do que se descobre no meio, é agente, com limites.",
                "prosa": [
                    "O quinto conceito junta os quatro numa pergunta: dá para escrever os passos antes de rodar? Os dois desenhos também se combinam: um workflow "
                    "que roteia e chama o agente só na categoria que precisa investigar.",
                ],
                "bancada": {
                    "tipo": "quiz", "h3": "Workflow ou agente?",
                    "p": "Para cada problema do Balcão, escolha o desenho. Use a pergunta: dá para escrever os passos antes?",
                    "opcoes": [["w", "Workflow"], ["a", "Agente com limites"]],
                    "itens": [
                        {"origem": "TCK-004", "t": "Como emito o relatório mensal de vendas por bandeira de cartão?", "r": "w",
                         "fb": "Passos conhecidos: classificar e responder com o artigo certo."},
                        {"origem": "TCK-011", "t": "O valor que caiu na conta veio menor que as vendas. Tarifa, antecipação ou erro?", "r": "a",
                         "fb": "O caminho depende do que aparecer: tarifa contratada, antecipação ou erro pedem investigações diferentes."},
                        {"origem": "Rotina", "t": "Extrair CNPJ, valor e data de toda nota fiscal que chega por e-mail.", "r": "w",
                         "fb": "Mesmos campos, mesma ordem, toda vez. Um agente só traria variação."},
                        {"origem": "TCK-005", "t": "E-mail de senha alterada que a cliente não pediu.", "r": "w",
                         "fb": "Caminho conhecido e urgente: classificar como acesso_conta P1 e passar para segurança. Investigar sozinho só atrasa."},
                        {"origem": "TCK-002", "t": "Cobrada duas vezes na mensalidade; quer o estorno de uma.", "r": "a",
                         "fb": "Na aula, agente: ele confirmou o lançamento e achou o mesmo padrão em outro cliente. Também defensável: um workflow com um passo fixo de "
                               "consulta de cobranças, se duplicidade for o único caso que aparece."},
                    ],
                },
                "pratica": "Pergunte por tipo de ticket, não pelo sistema inteiro. A mesma fila pode ter workflow para quatro categorias e agente para uma.",
                "pergunta": ("por que muita equipe começa pelo agente?",
                             "Porque impressiona na demonstração. O custo e a variação só aparecem com volume, em produção. Começar pelo workflow e subir com motivo evita essa conta."),
            },
        ],
        "demo": {
            "h2": "O workflow repete o caminho; o agente escolhe o que investigar",
            "prosa": [
                "<b>A tarefa:</b> triar e resolver tickets do Balcão. No <b>Ato 1</b>, o código fixa os passos e o modelo só classifica e redige. No <b>Ato 2</b>, "
                "o modelo recebe o objetivo e ferramentas de leitura e decide o que investigar.",
                "As saídas abaixo são <b>execuções reais</b>, registradas em 10/11/2026 com o claude-opus-5-5, cada uma numa conversa nova. O texto não foi editado. "
                "Na aula, o professor roda os mesmos pedidos com os scripts do caso.",
            ],
            "atos": [
                {
                    "tipo": "passos", "real": True, "selo": "Ato 1",
                    "h3": "Workflow: a mesma classificação em três tickets",
                    "p": "Conceitos à vista: 1 workflow e 3 custo previsível.",
                    "passos": [
                        {"t": "TCK-001 · maquininha parada", "e": "Débito parado desde as 9h, vendas perdidas agora.",
                         "c": {"lista": [ctx.pedido("m3a1-clas-TCK-001"), ctx.saida("m3a1-clas-TCK-001")]}},
                        {"t": "TCK-002 · cobrança duplicada", "e": "Mesma instrução, outro ticket.", "c": ctx.saida("m3a1-clas-TCK-002")},
                        {"t": "TCK-011 · farmácia, execução 1", "e": "O ticket ambíguo: tarifa, antecipação ou erro.",
                         "c": {"lista": [ctx.pedido("m3a1-clas-TCK-011"), ctx.saida("m3a1-clas-TCK-011", 1)]}},
                        {"t": "TCK-011 · farmácia, execução 2", "e": "O mesmo pedido, numa conversa nova.", "c": ctx.saida("m3a1-clas-TCK-011", 2)},
                        {"t": "O que isso mostra",
                         "e": "<b>As quatro classificações conferem com o gabarito</b>, e o TCK-011 deu o mesmo rótulo nas duas conversas. O caminho foi o mesmo em todos: "
                              "uma chamada, um JSON. Mas o workflow classificou a farmácia sem investigar se foi tarifa ou erro: isso não estava nos passos."},
                    ],
                    "vivo": "m3a1-clas-TCK-011", "vivo_rotulo": "Classificar o TCK-011 agora",
                },
                {
                    "tipo": "passos", "real": True, "selo": "Ato 2",
                    "h3": "Agente: duas execuções do mesmo pedido",
                    "p": "Conceitos à vista: 2 loop do agente, 3 variação e 4 parada. No botão ao vivo, a página oferece ao Claude duas ferramentas, listar e ler os arquivos do caso, e mostra cada chamada que ele decidir fazer.",
                    "agente": {"chave": "m3a1-agente-vivo", "titulo": "Rodar o agente agora, com ferramentas da página",
                               "rotulo": "Rodar o agente no TCK-002", "arquivos": ctx.arquivos},
                    "passos": [
                        {"t": "Execução 1 · as voltas", "e": "Listou a pasta, leu os três arquivos de uma vez e parou para escrever.", "c": voltas_html(ag1)},
                        {"t": "Execução 1 · a resposta", "e": "Repare no fim: além do Bazar Estrela, o agente apontou que a descrição do arquivo de cobranças dizia “outubro” e havia "
                                                              "um lançamento de novembro. Era um erro real do material, corrigido depois deste registro.",
                         "c": ctx.saida("m3a1-agente-TCK-002", 1)},
                        {"t": "Execução 2 · as voltas", "e": "O mesmo caminho da execução 1.", "c": voltas_html(ag2)},
                        {"t": "Execução 2 · a resposta", "e": "Mesmo diagnóstico, texto diferente: aqui o agente escreveu “vamos estornar”, e não que o estorno estava aprovado.",
                         "c": ctx.saida("m3a1-agente-TCK-002", 2)},
                        {"t": "O que isso mostra",
                         "e": "<b>O agente investigou o que o workflow não investigava, nas duas execuções.</b> O caminho se repetiu porque os dados são pequenos; "
                              "a variação apareceu no texto da resposta. É por isso que uma execução só não basta para avaliar um agente, tema do M4."},
                    ],
                },
            ],
        },
        "discussao": {
            "h2": "Investigar ou repetir: o que pesa mais?",
            "a": "O agente achou a duplicidade sozinho, conferiu a regra dos R$ 200 e ainda apontou o mesmo padrão no Bazar Estrela. Para cobrança contestada, isso poupa o tempo de uma pessoa.",
            "b": "O workflow fez a mesma coisa nos quatro casos, com uma chamada por passo, e dá para testar cada passo. Para dúvida de produto, investigar é desperdício.",
            "revelar": [
                ("Como seria um desenho híbrido no Balcão?",
                 "Um workflow classifica e roteia todos os tickets; só a categoria cobranca_indevida chama o agente, com leitura dos dados, teto de US$ 0,50 e escalada acima de R$ 200."),
                ("O agente prometeu estorno ao cliente na execução 1. Isso é problema?",
                 "É. Ele só tinha leitura e não emitiu nada, mas escreveu que o estorno “está aprovado”. A política de parada e as permissões não cuidam do texto; "
                 "isso é tema de guardrails, na aula 3 do M4."),
            ],
        },
        "cartao": {
            "ideias": [
                "No workflow, o código decide o caminho.",
                "No agente, o modelo decide o próximo passo, e o resultado volta para a janela.",
                "Cada passo a mais custa tempo, dinheiro e uma chance de errar.",
                "Política de parada: objetivo, tetos de passos, custo e tempo, e escalada.",
                "Workflow primeiro; agente quando o caminho se descobre no meio.",
            ],
            "chave": ("A pergunta que decide", "<b>Dá para escrever os passos antes de rodar?</b><br>Sim: workflow.<br>Não: agente, com ferramentas mínimas, política de parada e registro."),
            "checklist": ("Antes de colocar um agente para rodar", [
                "O objetivo é verificável?", "Quais ferramentas ele precisa, e só elas?", "Qual o teto de passos, custo e tempo?",
                "Quando ele passa o caso para uma pessoa?", "Onde fica o registro do que ele fez?",
            ]),
        },
        "fechamento": {
            "h2": "Dê autonomia quando o caminho se descobre no meio",
            "mapa": [
                ("O código decide o caminho", "Previsível, barato e testável, mas só faz o que está escrito."),
                ("O modelo decide o próximo passo", "Investiga o que ninguém escreveu, como a duplicidade do Bazar Estrela."),
                ("Erro e variação se acumulam", "Uma execução só não diz quanto o agente custa nem quanto acerta."),
                ("Limite escrito antes de rodar", "A política não deixa o agente mais esperto; limita o tamanho do erro."),
                ("A escolha é por tipo de problema", "A mesma fila pode ter workflow e agente."),
            ],
            "resposta": ("Quando não dá para escrever os passos antes", "Fora disso, workflow. E quando for agente, com política de parada e registro."),
            "proximo": "Segunda, 16/11: tool use e function calling. Antes, faça a prática 2 do estudo dirigido: rodar o TCK-002 como agente e ler o registro.",
        },
        "rodape": (
            "As saídas marcadas como registradas foram geradas em 10/11/2026 pelo modelo claude-opus-5-5, por subagentes do Claude Code, cada uma numa conversa nova. "
            "Nas classificações e na resposta ao cliente, o subagente não usou ferramentas e recebeu a instrução da chamada colada no pedido. Nas duas execuções do agente, "
            "o subagente usou só Read, Glob e Grep numa cópia da pasta de dados do caso. Todos os pedidos vieram precedidos de uma instrução de experimento, mostrada em cada "
            "pedido. O texto das respostas não foi editado. Depois do registro, a descrição de cobrancas.json foi corrigida para “outubro e novembro”, como a execução 1 apontou. "
            "As respostas ao vivo usam o Claude da conta de quem abre a página e podem vir de outro modelo. As bancadas de erro composto e de política de parada usam valores ilustrativos."
        ),
        "fontes": [
            'Anthropic. <a href="https://www.anthropic.com/engineering/building-effective-agents">Building effective agents</a>. 19/12/2024.',
            'Yao et al. <a href="https://arxiv.org/abs/2210.03629">ReAct: Synergizing Reasoning and Acting in Language Models</a>. ICLR 2023.',
            'Claude Code. <a href="https://code.claude.com/docs/en/headless">Modo não interativo (headless)</a> e <a href="https://code.claude.com/docs/en/cli-reference">referência da CLI</a>.',
        ],
    }
