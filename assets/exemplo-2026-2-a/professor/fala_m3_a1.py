"""Guia do professor da M3.1: fala detalhada por slide e passo a passo da demonstração.

Títulos, horários, âncoras, figuras e o Bastidor (a condução) vêm de preparacao/aulas/m3_a1.py.
Todo comando do passo a passo precisa estar também na PARTE2 de lá: o gerador confere.
"""

USO = [
    "Cada slide traz a figura do deck, o horário previsto, a âncora (a frase que a turma deve levar) e o roteiro de fala, "
    "escrito para ser dito em voz alta, em primeira pessoa. O texto é mais longo do que o tempo de cada slide comporta, de "
    "propósito: ele serve para dominar o raciocínio e escolher, na hora, o que dizer. O que está entre colchetes é ação, não "
    "fala. O quadro **Bastidor** traz o cuidado de condução e a fonte do que a fala afirma.",
    "A aula é expositiva: nenhum momento depende de resposta da turma. As perguntas da fala são retóricas ou vão para o chat, "
    "que o monitor filtra. A espinha é a cadeia de conceitos, cada um saindo do anterior; dizer essa ligação em voz alta a "
    "cada transição é o que dá fluidez. A **Parte 2**, no fim, é o passo a passo da demonstração dos slides 12 e 13: "
    "preparação, comandos com botão de copiar, o que aparece na tela, o que dizer e o que fazer se algo falhar. Ela não "
    "soma tempo novo.",
]

CASO = (
    "**TCK-002 · Estúdio Pilates Vida**: dois lançamentos de R$ 189,90 em 05/10 (COB-5002 e COB-5003); gabarito "
    "`cobranca_indevida`, P2, financeiro. **TCK-001 · Mercearia Dois Irmãos**: débito parado desde as 9h; `falha_transacao`, "
    "P1, pagamentos. **TCK-011 · Farmácia Bem Estar**: repasse menor que as vendas do dia; `cobranca_indevida`, P2, "
    "financeiro. **Política**: estorno só para cobrança duplicada ou tarifa sem contrato, comprovada nos lançamentos; até "
    "R$ 200,00 o atendimento emite, acima disso precisa de aprovação do financeiro; todo estorno gera nota com o id do lançamento."
)

FALAS = {
    1: {
        "fala": [
            "Boa noite, pessoal. Eu sou o Victor Freire e fico com vocês nas próximas seis aulas, as três do M3 e as três do M4. "
            "Antes de qualquer conteúdo, um acerto rápido: se alguém não estiver me ouvindo bem ou não estiver vendo a tela, "
            "escreva no chat agora. O [nome do monitor] está acompanhando o chat e me avisa. [Pausa de cinco segundos; olhar o chat privado.]",
            "Uma ponte com o que vocês já fizeram. No M1 vocês viram como escolher o tipo de solução para um problema, e no M2 "
            "montaram um RAG: um sistema que busca trechos de documentos e responde com evidência. Nos dois casos o modelo fazia "
            "uma coisa só: recebia um texto e devolvia outro. A partir de hoje isso muda. O modelo passa a agir: consultar dados, "
            "ler arquivos, decidir o que fazer em seguida.",
            "E aí aparece a primeira decisão de quem constrói esse tipo de sistema, que é o título da aula, aí na tela: quem decide "
            "o próximo passo, o código ou o modelo? Parece uma pergunta técnica pequena, mas ela define quanto o sistema custa, "
            "quanto ele varia de uma execução para outra e o quanto vocês conseguem explicar o que aconteceu depois. A pergunta "
            "que eu quero responder até as dez da noite é esta: quando vale dar autonomia ao modelo?",
        ],
    },
    2: {
        "fala": [
            "Antes do conteúdo, o mapa dos dois módulos, porque ele explica por que hoje começa onde começa. Na tela tem seis "
            "caixas em fila, uma por aula, e a seta vai da esquerda para a direita: cada aula usa o que a anterior construiu.",
            "O M3 são as três primeiras caixas. Hoje, workflow ou agente: quem decide o próximo passo. Na segunda, dia 16, tool "
            "use: como dar uma ferramenta ao modelo de um jeito que ele use bem, e o que acontece quando o contrato da ferramenta "
            "é mal escrito. Na quarta, dia 18, MCP, um padrão para plugar ferramentas em agentes, com registro e limite. Em uma "
            "frase: o M3 dá autonomia e ferramentas ao modelo.",
            "O M4 são as três últimas, de 23 a 30 de novembro, e elas cobram a conta dessa autonomia. Evals, para medir se o "
            "sistema funciona e se uma mudança melhorou. Logs e custo, para explicar o que aconteceu numa execução e quanto custou. "
            "E guardrails, a caixa azul no fim, para proteger o sistema do que pode dar errado. A última caixa está destacada "
            "porque é para lá que o curso inteiro caminha: um agente que dá para colocar em produção. Não vou detalhar o M4 hoje; "
            "guardem só a ideia. Autonomia agora, conta depois.",
        ],
    },
    3: {
        "fala": [
            "Agora, como cada aula vai funcionar, para ninguém ficar esperando a hora de abrir o terminal. A fila de quatro "
            "caixas na tela é o formato das seis noites.",
            "Primeira caixa: exposição. Eu apresento os conceitos em cadeia, um saindo do outro. Segunda: demonstração. Eu opero e "
            "vocês assistem; ninguém precisa abrir nada nem rodar nada durante a aula. Terceira: monitor. Às 21h15, toda aula, um "
            "monitor apresenta vinte minutos sobre um tema vizinho ao da noite; hoje é o LangGraph. Quarta caixa, a azul, que fica "
            "para depois da aula: o estudo dirigido. É um PDF por aula, com os conceitos detalhados, um glossário e três práticas "
            "passo a passo, todas no Claude Code, que vocês já têm.",
            "Os seis estudos já estão no repositório da turma, na pasta estudos-dirigidos, junto com o caso que a gente vai usar; "
            "o [nome do monitor] deixou o link no chat. O chat fica aberto a noite inteira. Ninguém precisa falar nem abrir câmera: "
            "escrevam ali. O monitor separa as perguntas e me passa nos momentos certos, principalmente na discussão, perto das "
            "21h35.",
        ],
    },
    4: {
        "fala": [
            "Para ninguém se perder trocando de exemplo a cada aula, as seis noites usam um caso só. O Balcão é uma plataforma "
            "fictícia de pagamentos para pequenos comércios: maquininha, link de pagamento e API para quem vende on-line. Pensem "
            "numa mercearia, num estúdio de pilates, numa farmácia de bairro. Esses são os clientes.",
            "O suporte do Balcão recebe tickets em texto livre e faz o caminho das cinco caixas na tela. O ticket chega. Alguém "
            "faz a triagem: dá uma categoria, como falha de transação ou cobrança indevida, e uma prioridade, de P1 a P3. Depois "
            "investiga nos dados: quem é o cliente, quais cobranças foram feitas, o que a política permite. Decide uma ação: "
            "registrar uma nota, emitir um estorno, encaminhar para outro time. E responde ao cliente, a caixa azul no fim.",
            "O material do caso é pequeno de propósito, para caber na cabeça: doze tickets, um arquivo de clientes, um de cobranças "
            "e a política de atendimento, que diz, por exemplo, que estorno de até duzentos reais o próprio atendimento pode emitir, "
            "e acima disso precisa de aprovação do financeiro. [Mostrar a pasta caso-balcao no explorador por trinta segundos.] "
            "Guardem um ticket, o TCK-002, do Estúdio Pilates Vida: “fui cobrada duas vezes da mensalidade do plano Pro em outubro; "
            "o extrato mostra dois lançamentos de R$ 189,90 no dia 05/10”. Ele volta na demonstração e nas próximas aulas.",
            "E a pergunta de hoje, aplicada ao caso: esse caminho de cinco caixas é um workflow ou um agente? Quem decide se, depois "
            "da triagem, vale olhar as cobranças ou a política: um programa escrito antes, ou o modelo, olhando o ticket? Guardem a "
            "pergunta. O mapa da aula, no próximo slide, é o caminho até a resposta.",
        ],
    },
    5: {
        "fala": [
            "Este é o slide para quem se perder em algum momento da noite: ele é o índice da aula. São cinco conceitos em fila, e "
            "cada um sai do anterior. Vou ler a fila da esquerda para a direita.",
            "Passo 1, workflow: o código decide o caminho. É o que vocês já conhecem do M2, mesmo sem esse nome. Passo 2, agente: o "
            "contrário, o modelo decide o próximo passo. Passo 3, custo: se o modelo decide quantos passos dar, cada passo a mais "
            "custa tempo, dinheiro e uma chance a mais de errar. Passo 4, parada: a resposta de engenharia ao passo 3, um limite "
            "escrito antes de rodar. Passo 5, escolha: os quatro viram uma regra, começar pelo workflow e subir para agente quando "
            "houver motivo.",
            "Na última caixa, a azul, está a pergunta da noite: quando dar autonomia ao modelo? Eu não vou responder agora. Ela "
            "volta na discussão, depois do monitor, e eu respondo no fechamento, refazendo esta mesma fila com uma frase por caixa.",
            "Uma dica de como acompanhar: a cada conceito novo, eu vou dizer em voz alta de qual ele saiu. Se em algum momento a "
            "ligação não fizer sentido, escrevam no chat algo como “não liguei o 3 com o 2”. O monitor me passa, e eu refaço a "
            "ponte antes de seguir.",
        ],
    },
    6: {
        "fala": [
            "Primeiro conceito, e eu começo pelo que vocês já conhecem. O RAG do M2 é um workflow: buscar os trechos, montar o "
            "contexto, gerar a resposta. Sempre nessa ordem, para qualquer pergunta. Ninguém pergunta ao modelo se ele quer buscar "
            "antes ou depois; o código já decidiu. **Workflow é código que chama o modelo em passos fixos**: a ordem, os desvios e o "
            "fim estão escritos antes de rodar.",
            "Agora no caso Balcão, na figura. Vou por passos, e reparem no tipo de borda de cada caixa. Passo 1: o ticket entra como "
            "texto. Passo 2, a caixa de borda tracejada: uma chamada ao modelo classifica o ticket em categoria e prioridade. A borda "
            "tracejada, em todas as figuras do curso, quer dizer “aqui quem trabalha é o modelo”. Passo 3, borda cheia: o "
            "roteamento. É uma regra no código, um dicionário: cobrança indevida vai para o financeiro, falha de transação vai para "
            "pagamentos. Sem modelo nenhum. Passo 4, tracejada de novo: outra chamada ao modelo escreve o rascunho da resposta. "
            "Passo 5, a caixa azul: o ticket chega à fila do time. Sempre três passos.",
            "A frase embaixo da figura é o que eu quero que fique: o modelo preenche os passos, mas quem escolhe o próximo passo é o "
            "código. O modelo pode ser sofisticado, pode até errar a categoria; quem decide o que acontece depois é o programa. Por "
            "isso, mesmo com um modelo de linguagem dentro, isto é workflow, não agente. É a confusão mais comum no mercado: chamar "
            "de agente qualquer coisa que tenha um LLM.",
            "Esse vocabulário não é meu. Em dezembro de 2024, a Anthropic publicou um texto que virou referência, “Building "
            "effective agents”, que define workflow assim: modelos e ferramentas orquestrados por caminhos de código predefinidos. O "
            "texto lista cinco padrões que cobrem quase tudo o que se faz com workflow. Encadeamento: a saída de uma chamada vira a "
            "entrada da próxima. Roteamento: uma classificação escolhe o caminho. Paralelização: várias chamadas ao mesmo tempo, e "
            "depois junta. Orquestrador e trabalhadores: uma chamada divide a tarefa, outras executam. Avaliador e otimizador: uma "
            "chamada gera, outra critica e pede revisão. A nossa triagem é encadeamento com roteamento.",
            "O que os cinco padrões têm em comum é o que importa hoje: dá para desenhar o fluxo antes de rodar. E, se dá para "
            "desenhar, dá para testar cada passo isolado, prever o custo multiplicando chamadas por tickets e explicar depois por que "
            "algo aconteceu. Guardem essa vantagem, porque o próximo conceito é exatamente o que a gente perde quando entrega o "
            "volante ao modelo.",
        ],
    },
    7: {
        "fala": [
            "Segundo conceito, o espelho do primeiro. No workflow, eu escrevi o caminho. Agora eu faço o contrário: entrego ao "
            "modelo um objetivo, resolva o TCK-002, e algumas ferramentas, como ler arquivos e consultar dados. E não digo a ordem. "
            "**Agente é um loop**: o modelo olha o objetivo e o que já aconteceu, escolhe uma ação, recebe o resultado e decide de novo.",
            "Vou percorrer a figura como se fosse uma execução. Passo 1, a primeira caixa: o objetivo. Passo 2, a caixa tracejada: o "
            "modelo decide a próxima ação, ou decide parar. Talvez ele queira ler as cobranças primeiro; talvez a política. Passo 3: "
            "a ferramenta executa. E reparem que quem executa é o código de vocês; o modelo só pede. Passo 4, a caixa azul: o "
            "resultado entra na janela de contexto, aquela do M2, e a seta de baixo volta para o modelo. Ele decide de novo, agora "
            "com mais informação na janela. A frase na seta resume: repete até o modelo decidir parar.",
            "Em código, isso é um while. Enquanto o modelo não disser que terminou: chame o modelo, execute o que ele pediu, devolva o "
            "resultado. São poucas linhas. Por isso a palavra agente assusta mais do que deveria: o mecanismo é simples; o que muda "
            "é quem decide.",
            "Esse padrão tem nome na pesquisa desde 2022: ReAct, de raciocinar e agir, um artigo de pesquisadores de Princeton e do "
            "Google. No experimento clássico do artigo, o modelo respondia perguntas usando uma busca na Wikipédia: pensava, pedia "
            "uma busca, lia o resultado, pensava de novo, pedia outra. E havia uma ação especial, finish, que era o modelo dizendo "
            "“terminei, a resposta é esta”. Guardem esse detalhe: no agente, até a decisão de parar é do modelo. Esse vai ser o "
            "problema do conceito quatro.",
            "E vocês usam um agente desses todo dia. O Claude Code é exatamente isso: um modelo num loop com ferramentas de ler, "
            "editar e rodar comandos. Quando vocês pedem uma mudança, ele decide sozinho quais arquivos abrir, o que testar e quando "
            "parar. Reparem na frase da tela: é o mesmo modelo nos dois casos. O que muda é quem segura o volante. E quem segura o "
            "volante decide também quantas voltas a execução vai dar.",
        ],
    },
    8: {
        "fala": [
            "Terceiro conceito, consequência direta da última frase. Se o modelo decide quantas voltas dar, o número de passos deixa "
            "de ser uma constante do programa e vira uma variável. E cada passo cobra três coisas. Tempo: cada volta é mais uma "
            "chamada, mais uma espera. Dinheiro: cada volta reenvia a janela inteira, que só cresce, porque os resultados das "
            "ferramentas vão se acumulando nela. E risco: cada passo é uma chance a mais de errar.",
            "A figura mostra o risco com uma conta, e eu vou fazer a conta devagar. Passo 1: imaginem que cada passo do agente acerta "
            "95% das vezes. Parece ótimo. Passo 2: uma execução de um passo acerta 95%. Passo 3: se a execução tem cinco passos e "
            "todos precisam dar certo, a chance é 0,95 multiplicado por ele mesmo cinco vezes: 77%. Passo 4: dez passos, 60%. Vinte "
            "passos, a caixa azul, 36%. É zero vírgula noventa e cinco elevado ao número de passos. Um passo que acerta quase sempre, "
            "repetido vinte vezes, vira uma execução que erra quase duas em cada três.",
            "Agora o cuidado, que está na linha pequena embaixo da figura: isso é ilustrativo. Passos reais não são independentes "
            "assim; às vezes um passo corrige o erro do anterior, às vezes um erro no começo contamina todo o resto. Não tomem esses "
            "números como medida de modelo nenhum. Tomem a direção, que aparece também em medições reais: em 2025, o METR, um "
            "instituto que avalia modelos de IA, mediu agentes em tarefas de software de tamanhos diferentes e viu a taxa de sucesso "
            "cair à medida que a tarefa fica mais longa. Tarefa curta, quase sempre; tarefa de horas, raramente.",
            "Tem um segundo efeito, e esse vocês vão ver na tela depois do intervalo. O mesmo ticket, rodado duas vezes pelo agente, "
            "pode levar três passos numa execução e seis na outra. Então custo e tempo deixam de ser um número e viram uma faixa. No "
            "workflow da triagem, são sempre duas chamadas ao modelo por ticket: dá para prever o custo de mil tickets multiplicando. "
            "No agente, eu só consigo dizer “entre tanto e tanto”.",
            "A frase para levar é a da âncora: autonomia não é de graça; a gente paga em tempo, em custo e em erro que se acumula. E, "
            "se o modelo pode dar quantas voltas quiser, alguém precisa dizer quando chega. É o próximo conceito.",
        ],
    },
    9: {
        "fala": [
            "Quarto conceito, a resposta de engenharia ao terceiro. Se cada volta custa e arrisca, alguém precisa decidir quando o "
            "loop termina. E, lembrando do ReAct, no agente puro quem decide parar é o próprio modelo. Isso não basta. **Política de "
            "parada** é a regra, escrita antes de rodar, que diz quando o loop termina, independentemente do que o modelo achar.",
            "A figura é o que acontece no fim de cada volta. Vou por passos. Passo 1, a primeira caixa: terminou uma volta. Passo 2, "
            "o losango amarelo, a pergunta: cumpriu a meta ou bateu um limite? Se sim, ramo de cima, caixa azul: para. E parar tem "
            "duas saídas: entregar a resposta ou passar para uma pessoa. Passo 3, se não: a caixa de borda verde pergunta se a volta "
            "trouxe algo novo para a janela. A borda verde, nas nossas figuras, é controle, uma verificação que não é do modelo. Se "
            "progrediu, passo 4, caixa tracejada: nova volta, e o modelo decide de novo. Se não progrediu, isso já é motivo para parar.",
            "Na prática, uma política de parada tem cinco campos, e eu quero que vocês saiam sabendo escrever os cinco. Um, o "
            "objetivo verificável: como eu sei que terminou? No TCK-002, categoria, verificação dos lançamentos e resposta ao cliente "
            "escritas. Dois, um teto de passos. Três, um teto de custo. Quatro, um teto de tempo. Cinco, a condição de passar para "
            "uma pessoa: duas voltas sem nada novo, ou uma ação sensível, como um estorno acima de duzentos reais, que a nossa "
            "política já manda para aprovação do financeiro.",
            "Por que o campo cinco importa tanto? Em julho de 2025, um caso ficou conhecido. O fundador da SaaStr, uma comunidade de "
            "empresas de software, construía um aplicativo com o agente da Replit e tinha declarado um congelamento: nenhuma mudança. "
            "O agente apagou o banco de dados de produção mesmo assim. O CEO da Replit chamou o caso de inaceitável, e a empresa "
            "anunciou a separação automática entre banco de desenvolvimento e de produção. O que faltou ali não foi capacidade do "
            "modelo; faltou uma regra, fora do modelo, dizendo que aquela ação passava por uma pessoa.",
            "No Claude Code, parte disso já vem como opção. Rodando sem interação, com menos p, eu limito o gasto em dólares com "
            "--max-budget-usd e o número de voltas com --max-turns. A documentação avisa um detalhe: o gasto é conferido depois que "
            "cada resposta do modelo chega, então a execução pode passar um pouco do teto. Na demonstração o agente roda com teto de "
            "cinquenta centavos de dólar, e eu vou mostrar uma execução cortada pelo teto. E reparem no que a política não faz: ela "
            "não deixa o agente mais inteligente. Ela garante que, quando ele errar, o erro tem tamanho máximo.",
        ],
        "bastidor": (
            "Caso Replit: SaaStr, julho de 2025, com cobertura de imprensa em 21–22/07/2025. Contar só o que está acima; os "
            "detalhes do que o agente “disse” depois vêm das capturas de tela do próprio fundador e não foram verificados."
        ),
    },
    10: {
        "fala": [
            "O quinto conceito junta os quatro numa pergunta só, que está no losango amarelo: dá para escrever os passos antes de "
            "rodar? Reparem que a primeira caixa não diz “o sistema”; diz “um tipo de ticket”. A decisão não é para o produto "
            "inteiro; é para cada tipo de problema.",
            "Dois exemplos do Balcão, um de cada ramo. Uma dúvida de produto, como “onde eu emito o relatório de vendas por "
            "bandeira?”: dá para escrever os passos antes. Classificar, responder com o artigo certo da ajuda, fim. Ramo de cima, "
            "caixa azul: workflow, previsível, barato e testável. Agora uma cobrança contestada, como a da farmácia, o TCK-011: “o "
            "valor que caiu veio menor do que o total das vendas; não sei se é tarifa, antecipação ou erro”. O caminho depende do "
            "que aparece no meio. Tem duplicidade? É tarifa de antecipação? Havia contrato de antecipação? Ninguém escreveria todos "
            "esses desvios antes. Ramo de baixo: agente com ferramentas, e sempre com a caixa verde, limites de parada, custo e registro.",
            "Isso vai contra um instinto comum. Muita equipe começa pelo agente porque impressiona na demo e só descobre o custo e a "
            "variação em produção. O mesmo texto da Anthropic de 2024 recomenda o contrário: procurar a solução mais simples possível "
            "e só aumentar a complexidade quando for preciso. E há um exemplo de pesquisa que eu gosto. Em 2024, pesquisadores da "
            "Universidade de Illinois publicaram o Agentless, literalmente “sem agente”, para corrigir bugs reais de projetos Python. "
            "Em vez de um agente decidindo o que fazer, um processo fixo: localizar onde está o problema, gerar candidatos de "
            "correção, escolher um pelos testes. No benchmark da época, ficou no nível dos melhores agentes de código aberto, "
            "custando menos por problema. Não quer dizer que workflow sempre vence; quer dizer que o agente precisa justificar o que "
            "custa a mais.",
            "Então a regra da noite: comece pelo mais simples que resolve e suba um degrau quando houver motivo, e o motivo é o "
            "caminho depender do que se descobre no meio. Depois do intervalo eu mostro os dois rodando no mesmo caso, e vocês vão "
            "ver na tela cada um dos cinco conceitos acontecendo.",
        ],
        "bastidor": "Agentless (Xia et al., 2024): citar sem números; os resultados valem para os modelos e o benchmark daquela época.",
    },
    11: {
        "fala": [
            "Paramos aqui. São quinze minutos de intervalo, e a gente volta às 20h25 em ponto.",
            "Uma recapitulação de dez segundos para levar para o café: workflow, o código decide; agente, o modelo decide; cada passo "
            "custa e arrisca; a parada é escrita antes; e a escolha é por tipo de problema. Na volta, eu paro de explicar e passo a "
            "mostrar: o mesmo caso rodando como workflow e como agente.",
            "Se tiver pergunta, escrevam no chat durante o intervalo. O [nome do monitor] separa as melhores para a discussão.",
        ],
        "bastidor": (
            "Nos quinze minutos: rodar de novo `claude -p \"responda apenas: ok\"`, abrir `workflow_triagem.py` no editor e deixar "
            "o terminal em `C:\\demo\\caso-balcao\\ferramentas` com fonte grande. Tudo na Parte 2."
        ),
    },
    12: {
        "fala": [
            "Bem-vindos de volta. Agora os conceitos acontecendo. Primeiro ato: o workflow. Na tela, as cinco caixas do ato: rodar "
            "o script em três tickets, classificar com saída em JSON, rotear no código, responder, e a caixa azul, o mesmo caminho "
            "para todo ticket. Os conceitos à vista são o um, workflow, e o três, custo, pelo lado bom.",
            "Começo pelo código, porque o workflow está escrito nele. [Abrir workflow_triagem.py.] Aqui no topo, o esquema da "
            "classificação: ele obriga a resposta a ser uma categoria da lista e uma prioridade entre P1, P2 e P3. Nada de texto "
            "livre. Aqui, o dicionário ROTA: categoria para time. Essa é a seta do código, sem modelo. E aqui a função triar, com "
            "os três passos na ordem: chamar o modelo para classificar, consultar o dicionário, chamar o modelo para responder. Cada "
            "chamada ao modelo é feita pelo próprio Claude Code em modo não interativo, rodando numa pasta vazia e sem ferramenta "
            "nenhuma. O mesmo Claude Code que é um agente, aqui usado como chamada simples de modelo. Isso já é uma lição: ser "
            "agente é o desenho, não a ferramenta.",
            "Para ver o que é uma chamada, faço uma isolada. [Rodar a chamada isolada.] Entra um texto, sai um JSON com a resposta, "
            "no campo result, o tempo em milissegundos e o custo estimado. Em assinatura do Claude, esse custo é estimativa do Claude "
            "Code; ninguém está sendo cobrado por chamada. Agora rodo o workflow em três tickets: a mercearia com a maquininha "
            "parada, o estúdio cobrado duas vezes e a farmácia que recebeu menos do que vendeu. [Rodar os três tickets.]",
            "Reparem na tabela. A coluna chamadas: dois, dois, dois. Sempre. O tempo e o custo ficam na mesma faixa de um ticket "
            "para o outro. A coluna gabarito compara com a resposta esperada do caso. Conceito um: o caminho é do código. Conceito "
            "três, pelo lado bom: dá para prever o custo de mil tickets multiplicando. E rodo duas vezes só a classificação da "
            "farmácia. O caminho é o mesmo nas duas: uma chamada e uma regra. Se o rótulo mudar entre elas, a variação está dentro "
            "do passo, não no caminho, e medir isso é assunto do M4.",
            "Agora o limite, que é a ponte para o segundo ato. Olhem a resposta da farmácia. O workflow classificou como cobrança "
            "indevida, mandou para o financeiro e escreveu uma resposta educada dizendo que o time vai verificar. Mas ninguém "
            "verificou nada. Ele não sabe se foi tarifa, antecipação ou erro, porque investigar não estava nos passos. O workflow "
            "faz bem o que está escrito, e só o que está escrito.",
        ],
    },
    13: {
        "fala": [
            "Segundo ato: o mesmo caso, agora com o agente, no TCK-002, o estúdio cobrado duas vezes. Na tela, as cinco caixas: o "
            "pedido com o objetivo e a pasta de dados; o agente decide o que ler, e reparem que essas caixas estão tracejadas, quem "
            "decide é o modelo; ele confere os lançamentos; eu rodo de novo para comparar; e a caixa azul, o registro de passos, "
            "tempo e custo. Os conceitos à vista são o dois, o três e o quatro.",
            "Primeiro, o que eu entrego ao agente. [Abrir rodar_agente.py.] O pedido diz o objetivo, resolver o ticket, onde estão "
            "os dados e o formato do fim: categoria e prioridade, o que verificou, a resposta ao cliente e a recomendação ao time. E "
            "diz para não alterar nada. As ferramentas: só leitura, ler, listar e buscar arquivos. Tudo o que não está liberado é "
            "negado sem perguntar. E o teto: cinquenta centavos de dólar. Reparem no que eu não digo: a ordem. Não digo “leia as "
            "cobranças e depois a política”. Isso é com ele. [Rodar a primeira execução.]",
            "Enquanto ele roda, a tela fica parada: o script só mostra o registro quando a execução termina. [Quando terminar, ler o "
            "resumo de cima para baixo.] Passo 1: ele pediu para listar a pasta. Passo 2: leu a política, os clientes e as cobranças. "
            "Ninguém escreveu esses passos; esse é o loop do conceito dois. No fim, a conclusão: dois lançamentos de R$ 189,90 no "
            "mesmo dia, 05/10; pela política cabe estorno, e como é menos de duzentos reais, o próprio atendimento pode emitir. E tem "
            "uma coisa que eu não pedi. [Mostrar a resposta inteira.] Nas execuções de preparação, o agente também notou que outro "
            "cliente, o Bazar Estrela, teve a mesma mensalidade cobrada duas vezes no mesmo dia, e sugeriu investigar a rotina de "
            "cobrança daquela data. O workflow nunca faria isso.",
            "Agora rodo de novo, o mesmo pedido, e comparo os dois resumos, uma linha cada. Conceito três. Com dados pequenos como "
            "os nossos, o caminho pode até se repetir; nas execuções de preparação, os dois caminhos foram iguais. Aí a variação "
            "aparece em outro lugar: no texto da resposta, no que ele resolveu comentar a mais, no tempo e no custo, que deixam de ser "
            "um número e viram uma faixa. Se hoje o caminho mudar, ótimo: é a variação aparecendo onde a gente esperava.",
            "Por último, o conceito quatro. Rodo o ticket da farmácia com um teto baixo, cinco centavos de dólar. A execução para no "
            "limite, e o registro mostra o motivo no fim: parada por orçamento, sem resposta final. É a política de parada "
            "funcionando: o erro tem tamanho máximo. Comparem com o primeiro ato. O agente investigou o que o workflow não "
            "investigava, achou o que ninguém pediu, e cobrou por isso em tempo, custo e variação. Essa é a troca da noite.",
        ],
    },
    14: {
        "fala": [
            "Agora eu passo a palavra ao [nome do monitor]. Hoje eu mostrei workflow e agente de dois jeitos: com um script em Python "
            "puro e com o Claude Code. Na indústria, muita gente monta esses dois desenhos com um framework, e o mais usado no "
            "ecossistema Python é o LangGraph.",
            "Ele vai mostrar o nosso caso, o Balcão, como um grafo de estados: o workflow da triagem como um grafo em linha, e o "
            "agente como um grafo com uma volta e um limite de passos. Prestem atenção em duas coisas: onde fica, no grafo, a seta "
            "que hoje era o dicionário ROTA, e onde fica a política de parada. São vinte minutos; perguntas no chat, como sempre.",
            "[Ao fim dos vinte minutos.] Obrigado, [nome do monitor]. Reparem que o framework não mudou nenhum conceito: no grafo, ou "
            "a aresta é fixa, e é workflow, ou ela volta enquanto o modelo pedir ferramenta, e é agente. O framework não decide se é "
            "workflow ou agente; o desenho decide.",
        ],
    },
    15: {
        "fala": [
            "Agora a discussão. Como combinamos, ninguém precisa falar: eu mesmo defendo os dois lados, um de cada vez, e no fim o "
            "[nome do monitor] traz as perguntas do chat. Na tela, duas caixas à esquerda, os dois argumentos, convergindo para a "
            "pergunta da noite, na caixa azul.",
            "Argumento A, a favor do agente: ele achou a duplicidade sozinho, conferiu na política se cabia estorno e quem podia "
            "emitir, e ainda apontou outro cliente com o mesmo problema. Para um ticket de cobrança, isso é a investigação que uma "
            "pessoa do financeiro faria, pronta antes de alguém abrir o ticket. Se a fila tem muitas contestações por mês, a "
            "investigação automática se paga.",
            "Argumento B, a favor do workflow: ele fez sempre a mesma coisa, custou menos e eu consigo testar e explicar cada passo. "
            "Se amanhã um cliente reclamar da resposta, eu sei exatamente qual chamada gerou qual frase. Para uma dúvida de produto, "
            "investigar é desperdício: o agente gastaria voltas lendo cobranças de quem só quer saber onde fica um relatório.",
            "Os dois estão certos, para tipos diferentes de ticket. Por isso a decisão não é da equipe, “aqui a gente usa agente”, "
            "nem da ferramenta, “o framework é de agente”. É de cada tipo de problema. E existe um desenho híbrido, muito comum: um "
            "workflow que classifica e roteia todo ticket e chama o agente só na categoria cobrança indevida, onde investigar vale "
            "a pena. [Ouvir do monitor até três perguntas do chat.]",
        ],
    },
    16: {
        "fala": [
            "Para fechar, eu refaço o mapa do começo da noite, agora com uma frase por caixa. A fila na tela é a mesma do slide cinco, "
            "com respostas no lugar das perguntas. Workflow: o código decide o caminho. Agente: o modelo decide o próximo passo. "
            "Custo: erro e variação se acumulam a cada volta. Parada: um limite escrito antes de rodar, fora do modelo. Escolha: por "
            "tipo de problema.",
            "E a caixa azul, a resposta à pergunta da noite: quando vale dar autonomia ao modelo? Quando o caminho se descobre no meio "
            "e não dá para escrever os passos antes. Fora disso, workflow. E, quando for agente, sempre com política de parada e com "
            "registro do que ele fez, como o registro que vocês viram na tela. O título resume: autonomia é decisão de projeto, não "
            "upgrade. Agente não é a versão melhorada do workflow; é outro desenho, com outro custo.",
            "Para depois da aula: o estudo dirigido de hoje está no repositório da turma, na pasta estudos-dirigidos. São três "
            "práticas no Claude Code: montar o workflow de triagem, rodar o mesmo ticket como agente e comparar, e escrever a "
            "política de parada de um agente do trabalho de vocês, com os cinco campos. A terceira é a mais importante: usem um "
            "caso real.",
            "Na segunda-feira, dia 16, a gente abre a caixa da ferramenta. Hoje o agente só leu arquivos. Na segunda a pergunta é: o "
            "que faz uma ferramenta ser boa para um modelo, e o que acontece quando o contrato dela é mal escrito. Obrigado pela "
            "noite, e até segunda.",
        ],
    },
}

PREPARO = [
    {
        "titulo": "Claude Code com login",
        "texto": "Tem de responder `ok`; `claude --version` não basta. Se aparecer “OAuth session expired”, rodar `claude`, entrar com `/login` e testar de novo.",
        "cmds": ['claude -p "responda apenas: ok"'],
    },
    {
        "titulo": "Python 3.11 ou mais novo",
        "texto": "Esta aula não precisa de pacote extra.",
        "cmds": ["python --version"],
    },
    {
        "titulo": "Cópia do caso e terminal com acentos",
        "texto": "Numa janela nova do PowerShell. A primeira linha apaga a cópia anterior em `C:\\demo`; a fonte continua na pasta do curso.",
        "cmds": [
            r"Remove-Item -Recurse -Force C:\demo\caso-balcao -ErrorAction SilentlyContinue",
            'Copy-Item -Recurse -Force "$HOME\\iCloudDrive\\Trabalho\\CESAR\\Aulas\\Sistemas-IA-para-Devs\\2026.2-A\\material-alunos\\caso-balcao" C:\\demo\\',
            "[Console]::OutputEncoding = [Text.Encoding]::UTF8",
            '$env:PYTHONUTF8 = "1"',
            r"cd C:\demo\caso-balcao\ferramentas",
        ],
    },
    {
        "titulo": "Ensaio, que vira a contingência",
        "texto": "Rodar os dois atos uma vez e guardar as saídas. Anotar tempo, custo e voltas de cada execução: são a referência para comparar ao vivo.",
        "cmds": [
            r"New-Item -ItemType Directory -Force C:\demo\ensaio | Out-Null",
            r"python workflow_triagem.py TCK-001 TCK-002 TCK-011 | Tee-Object C:\demo\ensaio\ato1.txt",
            r"python rodar_agente.py --ticket TCK-002 --modo arquivos --saida C:\demo\ensaio\ato2-1.jsonl",
            r"python rodar_agente.py --ticket TCK-002 --modo arquivos --saida C:\demo\ensaio\ato2-2.jsonl",
            r"python rodar_agente.py --ticket TCK-011 --modo arquivos --orcamento 0.05 --saida C:\demo\ensaio\ato2-teto.jsonl",
        ],
    },
    {
        "titulo": "Tela",
        "texto": (
            "Fonte do terminal ampliada; `workflow_triagem.py` e `rodar_agente.py` abertos no editor; notificações silenciadas. "
            "À mão: o deck, este guia e o guia interativo da aula, na seção Demonstração."
        ),
        "cmds": [],
    },
]

ATOS = [
    {
        "slide": 12,
        "titulo": "Ato 1 · o workflow faz sempre os mesmos passos",
        "passos": [
            {
                "min": 4, "titulo": "Mostrar os três passos no código",
                "fazer": (
                    "No editor, em `workflow_triagem.py`: o `SCHEMA` (categoria só da lista de `tickets.json`, prioridade só P1, "
                    "P2 ou P3), o dicionário `ROTA` e a função `triar`, com as duas chamadas a `chamar` e o `ROTA.get` entre "
                    "elas. Em `claude_cli.py`, mostrar que `chamar` roda `claude -p` numa pasta temporária vazia, com "
                    "`--permission-mode dontAsk` e nenhuma ferramenta liberada."
                ),
                "dizer": "“O modelo aparece duas vezes, nas chamadas. A decisão de para onde vai o ticket é uma linha de Python.”",
            },
            {
                "min": 3, "titulo": "Uma chamada isolada",
                "cmds": ['claude -p "Classifique este ticket em uma palavra: maquininha não passa débito desde as 9h." --output-format json'],
                "tela": (
                    "Um JSON numa linha só. Apontar `result` (a resposta), `duration_ms` (tempo), `total_cost_usd` (custo "
                    "estimado) e `num_turns`. O campo `structured_output` só aparece quando há `--json-schema`, como nas "
                    "chamadas do script."
                ),
                "dizer": "“Isto é uma chamada: entra texto, sai texto, com tempo e custo. O workflow é código encadeando chamadas assim.”",
                "senao": "Erro de login ou mais de 30 segundos sem resposta: seguir para o passo 3 com a saída do ensaio.",
            },
            {
                "min": 8, "titulo": "Rodar o workflow em três tickets",
                "cmds": ["python workflow_triagem.py TCK-001 TCK-002 TCK-011"],
                "fazer": (
                    "São seis chamadas ao modelo, uma de cada vez. Durante a espera, ler os três tickets em voz alta: a Mercearia "
                    "Dois Irmãos sem débito desde as 9h, o Estúdio Pilates Vida cobrado duas vezes, a Farmácia Bem Estar que "
                    "recebeu menos do que vendeu."
                ),
                "tela": (
                    "Cabeçalho `ticket categoria prior. time gabarito chamadas tempo custo US$`, uma linha por ticket com a "
                    "`resposta:` embaixo e, no fim, o resumo: quantos conferem com o gabarito, tempo p50 e p95, custo total e "
                    "custo por acerto. Nas classificações registradas em 10/11: TCK-001 `falha_transacao` P1 (pagamentos); "
                    "TCK-002 e TCK-011 `cobranca_indevida` P2 (financeiro). As três iguais ao gabarito."
                ),
                "dizer": (
                    "“Chamadas: dois, dois, dois. Tempo e custo na mesma faixa. Para mil tickets, eu multiplico.” Na resposta da "
                    "farmácia: “ele promete verificar, mas ninguém verificou nada”."
                ),
                "senao": "Se uma linha vier `difere`, mostrar sem corrigir: é o gancho do M4, que mede isso com eval.",
            },
            {
                "min": 5, "titulo": "Repetir só a classificação do TCK-011",
                "cmds": ["python workflow_triagem.py TCK-011 --sem-resposta", "python workflow_triagem.py TCK-011 --sem-resposta"],
                "tela": (
                    "Uma linha por execução, agora com `chamadas` igual a 1: `--sem-resposta` pula o passo 3. Nas duas execuções "
                    "registradas em 10/11 deu `cobranca_indevida` e P2."
                ),
                "dizer": "“O caminho é o mesmo nas duas: uma chamada, uma regra. Se o rótulo mudar, a variação está dentro do passo, não no caminho.”",
            },
            {
                "min": 5, "titulo": "Fechar o ato",
                "fazer": "Voltar ao slide 12 e nomear os conceitos, um por frase.",
                "dizer": (
                    "“Um: o caminho é do código. Três, pelo lado bom: custo e tempo previsíveis. E o limite: a farmácia foi "
                    "classificada e roteada, mas não investigada.”"
                ),
            },
        ],
    },
    {
        "slide": 13,
        "titulo": "Ato 2 · o agente escolhe o que investigar",
        "passos": [
            {
                "min": 3, "titulo": "Mostrar o pedido, as ferramentas e o teto",
                "fazer": (
                    "Em `rodar_agente.py`: `PEDIDO_ARQUIVOS` (objetivo, os três arquivos, os quatro itens do fim e “não altere "
                    "nenhum arquivo”), `LEITURA` (`Read`, `Glob`, `Grep`) e o comando montado em `main`: `--output-format "
                    "stream-json --verbose` (o registro passo a passo), `--permission-mode dontAsk` (o que não está liberado é "
                    "negado sem perguntar), `--max-budget-usd` com o padrão de 0,50 e a pasta `dados` como diretório de trabalho."
                ),
                "dizer": "“Eu dou objetivo, ferramentas de leitura e um teto. Não digo a ordem.”",
            },
            {
                "min": 7, "titulo": "Primeira execução do TCK-002",
                "cmds": [
                    "python rodar_agente.py --ticket TCK-002 --modo arquivos --saida a1-ato2-1.jsonl",
                    "(Get-Content a1-ato2-1.jsonl -Encoding UTF8 | Select-Object -Last 1 | ConvertFrom-Json).result",
                ],
                "fazer": (
                    "O pedido aparece no topo; depois a tela fica parada em “Rodando o agente” até a execução terminar, porque o "
                    "resumo só sai no fim. Usar a espera para ler o pedido em voz alta. Ao terminar, ler o resumo de cima para "
                    "baixo. A segunda linha mostra a resposta inteira: o resumo corta em 400 caracteres, e as recomendações ao "
                    "time ficam no fim."
                ),
                "tela": (
                    "`Modelo:`, depois `Passo 1 · o modelo pede Glob …`, `Passo 2 · o modelo pede Read …`, cada um com a linha "
                    "`volta:`; no fim, `Fim: success · voltas: …`, tempo total contra tempo esperando a API, tokens, `Custo "
                    "estimado` e `Resposta final`. Nas duas execuções de preparação (10/11): primeiro `Glob **/*`, depois os três "
                    "`Read` (política, clientes, cobranças) numa volta só. Conclusão: COB-5002 e COB-5003, ambos de 05/10 e "
                    "R$ 189,90; estorno do COB-5003 pelo próprio atendimento, com nota. Sem o pedido mandar: a mesma duplicidade "
                    "no Bazar Estrela (COB-5011 e COB-5012, R$ 89,90) e três tarifas de antecipação sem contrato da Loja Bela Casa "
                    "(COB-5006 a COB-5008)."
                ),
                "dizer": "“Ninguém escreveu esses passos: ele decidiu listar, ler e conferir. É o loop do conceito dois.”",
                "senao": (
                    "Se ele resolver sem ler a política: apontar a lacuna. A política diz que todo estorno gera nota e que acima "
                    "de R$ 200 precisa de aprovação; sem ler, ele acertou por acaso, não por regra. Se ele tentar editar um "
                    "arquivo: mostrar a linha `ERRO` do passo, a negação de quem só tem leitura."
                ),
            },
            {
                "min": 6, "titulo": "Segunda execução e comparação",
                "cmds": [
                    "python rodar_agente.py --ticket TCK-002 --modo arquivos --saida a1-ato2-2.jsonl",
                    "python ler_execucao.py a1-ato2-1.jsonl --json",
                    "python ler_execucao.py a1-ato2-2.jsonl --json",
                ],
                "fazer": "Durante a espera, retomar o conceito três: o número de passos é variável, e custo e tempo viram faixa.",
                "tela": (
                    "Duas linhas JSON, uma por execução: `subtype`, `voltas`, `ferramentas` (a ordem das chamadas), `ms`, "
                    "`ms_api`, `custo_usd` e tokens. Comparar campo a campo. Nas execuções de preparação o caminho foi o mesmo "
                    "nas duas; o texto mudou (só uma apontou que o COB-5010 tem data fora de outubro)."
                ),
                "dizer": "“Com dados pequenos, o caminho pode se repetir. A variação aparece no texto, no tempo e no custo.”",
            },
            {
                "min": 5, "titulo": "Parada por orçamento",
                "cmds": ["python rodar_agente.py --ticket TCK-011 --modo arquivos --orcamento 0.05 --saida a1-ato2-teto.jsonl"],
                "tela": (
                    "O cabeçalho mostra `teto US$ 0.05`. No fim, `Fim: error_max_budget_usd` (nome da documentação do Agent SDK; "
                    "conferir no ensaio) e nenhuma linha `Resposta final`: só a execução que termina em `success` traz resposta. "
                    "O custo estimado pode passar um pouco de 0,05, porque o gasto é conferido depois que cada resposta chega."
                ),
                "dizer": "“Parou no limite, com o motivo registrado. A política não deixou o agente mais esperto; ela limitou o tamanho do erro.”",
                "senao": "Se terminar em `success`, rodar de novo com `--orcamento 0.01`.",
            },
            {
                "min": 4, "titulo": "Fechar o ato",
                "fazer": "Voltar ao slide 13. Se o agente demorou, este é o tempo de folga do ato.",
                "dizer": (
                    "“Dois: o agente escolheu o caminho. Três: investigou e achou o que ninguém pediu, e custo e tempo viraram "
                    "faixa. Quatro: com teto, parou no limite.”"
                ),
            },
        ],
    },
]

CONTINGENCIA = [
    {
        "titulo": "Sem rede ou sem login no Claude Code",
        "texto": (
            "Mostrar o ensaio. O `ler_execucao.py` não chama o modelo, então apresenta o registro do ensaio igual ao ao vivo. "
            "Dizer à turma: “são execuções reais do ensaio de hoje, com estes mesmos scripts”."
        ),
        "cmds": [
            r"Get-Content C:\demo\ensaio\ato1.txt",
            r"python ler_execucao.py C:\demo\ensaio\ato2-1.jsonl",
            r"python ler_execucao.py C:\demo\ensaio\ato2-teto.jsonl",
        ],
    },
    {
        "titulo": "Sem ensaio",
        "texto": (
            "Abrir a seção Demonstração do guia interativo da aula e dizer exatamente isto: são execuções registradas em 10/11 por "
            "um modelo Claude numa sessão de preparação, não por estes scripts; por isso não têm tempo nem custo."
        ),
        "cmds": [],
    },
]

REFS = [
    "SCHLUNTZ, Erik; ZHANG, Barry. *Building effective agents*. Anthropic, 19 dez. 2024. anthropic.com/engineering/building-effective-agents (slides 6, 9 e 10).",
    "YAO, Shunyu et al. *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023. arXiv:2210.03629 (slide 7).",
    "KWA, Thomas; WEST, Ben; BECKER, Joel et al. *Measuring AI Ability to Complete Long Tasks*. METR, mar. 2025. arXiv:2503.14499 (slide 8).",
    "XIA, Chunqiu Steven; DENG, Yinlin; DUNN, Soren; ZHANG, Lingming. *Agentless: Demystifying LLM-based Software Engineering Agents*. arXiv:2407.01489, 2024; FSE 2025 (slide 10).",
    "Incidente Replit e SaaStr, jul. 2025: cobertura de The Register, Tom’s Hardware e Gizmodo, 21–22 jul. 2025 (slide 9).",
    "Claude Code, referência da CLI (code.claude.com/docs/en/cli-reference): `--max-budget-usd`, `--max-turns`, `--json-schema`, `--permission-mode`, `--no-session-persistence`; e Agent SDK, “Handle the result” (code.claude.com/docs/en/agent-sdk/agent-loop): subtipos `success`, `error_max_turns`, `error_max_budget_usd` e conferência do gasto depois de cada resposta. Consultados em 11/11/2026 (slides 9, 12 e 13).",
    "Material da disciplina: `material-alunos/caso-balcao` (tickets, dados e scripts) e as execuções registradas em 10/11/2026 em `preparacao/guias/execucoes.json`.",
]

NOTA = (
    "A tabela de erro composto do slide 8 é ilustrativa. METR e Agentless entram como direção, sem números: os resultados "
    "valem para os modelos, as tarefas e as datas daqueles estudos. Tempo e custo da demonstração só existem quando medidos na "
    "hora ou no ensaio; este guia não traz nenhum."
)
