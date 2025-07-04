import requests
import pandas as pd
import openai
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--openai_key", type=str, required=True, help="Chave da API da OpenAI")
args = parser.parse_args()

openai.api_key = args.openai_key
API_URL = "http://127.0.0.1:8000/predict"

user_data_path = "../data/SPMQA Data Visualization - Sheet1.csv"  
df_users = pd.read_csv(user_data_path)

def obter_dado_float(pergunta):
    while True:
        try:
            return float(input(pergunta + ": ").replace(",", "."))
        except ValueError:
            print("Por favor, digite um número válido.")

def obter_dado_int(pergunta):
    while True:
        try:
            return int(input(pergunta + ": "))
        except ValueError:
            print("Por favor, digite um número inteiro válido.")

def obter_usuario():
    """Função para buscar o histórico de um usuário a partir do Roll No"""
    roll_no = input("Digite seu Roll No: ")
    usuario = df_users[df_users['Roll No'] == roll_no]
    
    if usuario.empty:
        print("Usuário não encontrado. Tente novamente.")
        return obter_usuario()
    
    # Retorna os dados do usuário, como as ferramentas escolhidas
    return usuario.iloc[0]

def gerar_sugestao_gpt4(pergunta):
    """Função para gerar sugestão com GPT-4 usando a API da OpenAI"""
    response = openai.ChatCompletion.create(
        model="gpt-4",  
        messages=[
            {"role": "system", "content": "Você é um assistente que ajuda a prever o sucesso de projetos."},
            {"role": "user", "content": pergunta}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()

def main():
    print("🧠 Chatbot de Previsão de Sucesso de Projetos")
    print("-------------------------------------------")

    project_cost = obter_dado_float("Digite o custo estimado do projeto (R$)")
    project_benefit = obter_dado_float("Digite o benefício estimado do projeto (R$)")
    year = obter_dado_int("Ano de início do projeto")
    month = obter_dado_int("Mês de início do projeto")


    roi = (project_benefit - project_cost) / project_cost

    usuario = obter_usuario()
    
    ferramentas = [usuario['Tool 1'], usuario['Tool 2'], usuario['Tool 3']]
    ferramentas_selecionadas = ", ".join([tool for tool in ferramentas if isinstance(tool, str)])

    payload = {
        "project_cost": project_cost,
        "project_benefit": project_benefit,
        "roi": roi,
        "year": year,
        "month": month
    }

    print("\n🔄 Enviando dados ao modelo...")
    try:
    
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        resultado = response.json()

        print("\n✅ Relatório do Projeto:")
        print(f"Ferramentas Selecionadas: {ferramentas_selecionadas}")
        print(f"Probabilidade de Sucesso: {resultado['success_probability']}%")
        print(f"Diagnóstico: {resultado['prediction']}")

        if project_cost < 1000000:
            print("🔧 Sugestão: Seu orçamento está abaixo da média dos projetos de sucesso. Considere ajustá-lo.")

        # Gerar uma sugestão personalizada com GPT-4
        pergunta_gpt4 = f"Com base nas ferramentas {ferramentas_selecionadas}, o projeto com custo de {project_cost} e benefício de {project_benefit}, qual seria a recomendação de melhoria?"
        sugestao_gpt4 = gerar_sugestao_gpt4(pergunta_gpt4)
        print(f"\n💬 Sugestão do Chatbot (GPT-4): {sugestao_gpt4}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao se comunicar com a API: {e}")

if __name__ == "__main__":
    main()