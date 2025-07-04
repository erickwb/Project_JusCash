# Como executar API

1. Entre na pasta da API e execute o comando:

    ```bash
    uvicorn main:app --reload
    ```

2. Agora, você pode acessar a API localmente através do seguinte endereço em seu navegador:

    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

    Isso abrirá a documentação interativa da API.

3. Exemplo de entrada no formato JSON:

    Aqui está um exemplo de como a entrada de dados para a API pode ser estruturada:

    ```json
    {
      "project_cost": 500000,
      "project_benefit": 800000,
      "roi": 0.6,
      "year": 2023,
      "month": 6,
      "team_size": 10
    }
    ```

4. Exemplo de saída da API:

    ```json
    {
      "success_probability": 85.0,
      "prediction": "Sucesso"
    }
    ```

# Como executar o Chatbot

1. Antes de executar o chatbot, você precisa garantir que a API (onde o modelo de aprendizado de máquina está hospedado) está rodando. Se a API não estiver rodando, inicie-a executando o seguinte comando na pasta `api`:

    ```bash
    uvicorn main:app --reload
    ```

2. Agora, com a API rodando, execute o script do chatbot:

    ```bash
    python chatbot_cli.py --openai_key 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
    ```

    O chatbot irá interagir com você e pedir os dados necessários para fazer a previsão de sucesso do projeto.

3. O Chatbot pedirá as seguintes informações:

    O script irá solicitar que você forneça os seguintes dados do projeto:

    - Digite o custo estimado do projeto (R$): 500000
    - Digite o benefício estimado do projeto (R$): 800000
    - Ano de início do projeto: 2023
    - Mês de início do projeto: 6
    - Digite seu Roll No: 20BCM019

4. Saída do Chatbot:

    Após fornecer os dados, o chatbot enviará esses dados para a API para fazer a previsão, e você receberá a saída com a probabilidade de sucesso e o diagnóstico. A saída será algo como:

    ```
    🔄 Enviando dados ao modelo...
    ✅ Relatório do Projeto:
    Ferramentas Selecionadas: ClickUp, Airtable, Trello
    Probabilidade de Sucesso: 23.71%
    Diagnóstico: Fracasso
    🔧 Sugestão: Seu orçamento está abaixo da média dos projetos de sucesso. Considere ajustá-lo.
    💬 Sugestão do Chatbot (GPT-4): Com base nas ferramentas ClickUp, Airtable, Trello e no custo 5000.0 e benefício 3000.0, o que você recomendaria para o projeto?
    ```
