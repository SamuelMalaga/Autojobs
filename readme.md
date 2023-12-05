# Linkedin job tracker


### Situação As is:
A pessoa acessa o linkedin, pega informações da vaga, acessa o link de aplicação (ou faz o easy apply), envia o currículo e finaliza a aplicação. O processo em sí não é nada complexo e pode ser feito manualmente porém é bem chatinho, além disso, quando a candidatura do link é fora do linkedin, você precisa lembrar se você se candidatou ou não, isso acaba fazendo que a pessoa perca tempo, talvez até responda algumas perguntas novamente, para então descobrir que já havia se aplicado para a vaga. Além disso, quando a pessoa se aplica, é bom que ela adeque seu currículo a descrição da vaga, isso é algo bem chato de fazer e bem repetitivo.

### Problemas
- Não tem o tracking das vagas aplicadas
- O processo é bem trabalhoso e moroso
- Existe muito potêncial de automação para a aplicação

### Proposta
- Um bot que consegue fazer o scrape de vagas no linkedin de acordo com o nome da vaga, local dela e tipo de trabalho
- Um software de processamento para iterar sobre as descrições, fazer prompts e gerar pdf's
- Uma interface para interação com esse software (pode ser gráfica ou prompt)

### Produtos finais (V1):
- Webscraper bot:
  - Bot de coleta de dados do linkedin de acordo com parâmetros passados (coleta de dados)
  - Bot de coleta de dados do linkedin de acordo com um link passado (refinamento de dados)
- API Django:
  - Manipulação e interação com os dados obtidos pelo scraper
  - Interação com o chat GPT:
    - Se não for possível fazer a interação direta com o GPT pelo django, ao menos fazer uma sugestão de prompt
    - Gerador de PDF (currículos gerados de acordo com a descrição da vaga)
- Base de dados para armazenar as informações que serão manipuladas
  - Armazenar as informações obtidas pelo bot
  - Armazenar as informações manipuladas dentro do app
  - Armazenar os currículos gerados
### Caminho de construção
1. Criar bot de para obtenção dos jobs
2. Criar a API para interação com banco de dados e com o front
3. Criar o front para mainpulação dos dados

### Documentos auxiliares
- Diagrama arquitetural do sistema
- Relacionamento de dados
- Diagrama de classes

### Requisitos API
- Configurar tabelas:
  - Lista de tabelas:
    - JobsAPI_application:
      - Status: OK
      - Descrição: tabela de relacionamento entre user e job, será o model principal iterado pelo front e com capacidade de armazenar os currículos gerados para cada vaga
    - JobsAPI_certification:
      - Status: OK
      - Descrição:
    - JobsAPI_job:
      - Status: OK
      - Descrição:
    - JobsAPI_education:
      - Status: OK
      - Descrição:
    - JobsAPI_language:
      - Status: OK
      - Descrição:
    - JobsAPI_workexperience:
      - Status: OK
      - Descrição:
    - Extensão da tabela usuário para adição das informações de country, city e bio:
      - Status: OK, ao invés de criar uma extensão da classe user padrão do django, foi criada uma tabela chamada userProfile com relação de 1 pra 1 com User, pode ser que futuramente seja necessário alterar
      - Descrição:
- Endpoints e urls para alterações de todas os models acima:
  - Lista de models para serem manipulados via views:
    - Application: OK
      - Get all:
      - GET OK
      - UPDATE OK
      - DELETE OK
    - Certification: OK
      - Get all:
      - GET
      - SET
      - UPDATE
      - DELETE
    - Job OK
      - job_list: OK
      - job_details:
        - GET: OK
        - PUT: OK
        - DELETE: OK
    - Education OK:
      - GET
      - SET
      - UPDATE
      - DELETE
    - Language OK:
      - GET
      - SET
      - UPDATE
      - DELETE
    - Workexperience OK:
      - GET
      - SET
      - UPDATE
      - DELETE
    - SCRAPER: OK
      - Execute scraper assíncrono, pesquisar django channel ou celery
- Integração com GPT (Fica pra V2):
  - Executar prompt usando o GPT
  - Retornar resultado de um prompt executado
  - Caso o uso de GPT seja custoso/caro, é necessário mudar a proposta para sugerir possíveis prompts e geração de pdf
- Geração de PDF's (currículos) (Entra na v1 porém só depois do front)

### Requisitos Front End
- Login? (estudar se é necessário nessa primeira implementação do front - Provável que sim)
- My Resumé: Página/formulários para CRUD das informações do currículo
  - Features:
    - CRUD experiências de trabalho
    - CRUD cursos/educações/projetos
    - CRUD linguagens
    - CRUD Certificações
    - CRUD Informações extras do perfil
    - Gerar Relatório?
- Job Tracker: Página para gerenciamneto dos jobs para os quais eu me apliquei (JobTracker)
  - Features:
    - Kanban View das applications:
      - Nessa página, uma visão de boards kanban seria o ideal, podendo arrastar de um lado para o outro e mudar o status de cada aplicação por meio dessa ação
      - Colunas:
        - Screening
        - Interview
        - Technical Interview
        - Inital interview
        - Techincal Assessment
        - Proposal
        - Cancelled
    - Botão/Form para adicionar um job via Link do linkedin:
      - Essa feature implica em uma execução do scraper pela API passando parametros e talvez seja assíncrona
- Dashboards: Página com análises de aproveitamento das aplicações, serve para entender bottlenecks, statuses e alguns pontos fracos de candidaturas e etc...

### Otimizações mapeadas durante o desenvolvimento para a primeira rodada de refatoração
- API: Juntar as views relacionadas aos mesmos models em classes, assim evita a necessidade de imports redundantes e marcações desnecessárias (Class Based Views)
- FrontEnd: modularizar a passagem de informação para os modais (estudar possibilidade de modal único ou criação de um módulo utils)
- Scraper: Criar uma ferramenta de log do scraper
