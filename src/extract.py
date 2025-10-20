import requests
import pandas as pd
import os

# URL do dado bruto de COVID-19 no Brasil
DATA_URL = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities.csv"
# Caminho onde salvaremos o dado bruto (camada "bronze")
RAW_DATA_PATH = os.path.join("data", "raw_cases_covid.csv")

def extract_data():
    """
    Extrai os dados de COVID-19 da URL e salva em um arquivo CSV bruto.
    """
    print("Iniciando extração de dados...")
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status() # Levanta um erro para respostas HTTP ruins

        # Cria o diretório 'data' se não existir
        os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
        
        # Salva o conteúdo bruto
        with open(RAW_DATA_PATH, 'wb') as f:
            f.write(response.content)
            
        print(f"Dados brutos salvos com sucesso em: {RAW_DATA_PATH}")
        return RAW_DATA_PATH
    
    except requests.RequestException as e:
        print(f"Erro ao baixar os dados: {e}")
        return None

if __name__ == "__main__":
    extract_data()