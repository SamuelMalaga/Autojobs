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
- Pegar todos os jobs (OK)
- Adicionar um job (OK)
- Editar um job (OK)
- Excluir um job (OK)
- Rodar o scraper (OK) | Revisar o mecanismo
- Receber input de perfil de usuário (currículo e dados do currículo) | Estudar como fazer a separação dessas informações ---> 4 tabelas, Work_experiece (OK), education (TODO), LANGUAGES (TODO), certifications (TODO), implementar classe de usuário para receber novas colunas (Bio, country e city) (TODO)
- Executar prompt usando o GPT
- Retornar resultado de um prompt executado
