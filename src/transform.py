import pandas as pd
import os

RAW_DATA_PATH = os.path.join("data", "raw_cases_covid.csv")
CLEAN_DATA_PATH = os.path.join("data", "clean_cases_covid.parquet") # Usaremos Parquet!

def transform_data(raw_path):
    """
    Lê os dados brutos, limpa, transforma e salva como Parquet.
    """
    print(f"Iniciando transformação dos dados de: {raw_path}")
    
    if not os.path.exists(raw_path):
        print(f"Arquivo bruto não encontrado: {raw_path}")
        return None

    # Ler os dados brutos (camada Bronze)
    df = pd.read_csv(raw_path, parse_dates=['date'])
    
    # 1. Renomear colunas para um padrão (ex: tudo minúsculo)
    df.columns = [col.lower().replace('/', '_') for col in df.columns]
    
    # 2. Selecionar apenas colunas relevantes
    # (Exemplo: vamos focar em casos e mortes totais)
    colunas_relevantes = [
        'date', 
        'state', 
        'city', 
        'ibgeid', 
        'totalcases', 
        'deaths'
    ]
    df_clean = df[colunas_relevantes].copy()

    # 3. Tratar tipos de dados (ibgeid deve ser string, pois não é número para cálculo)
    # Cuidado: Cidades podem ter 'ibgeID' nulo (ex: "Importados/Indefinidos")
    df_clean['ibgeid'] = df_clean['ibgeid'].astype(str).str.replace('.0', '', regex=False)

    # 4. Tratar valores nulos (ex: preencher 'city' nula com 'Indefinido')
    df_clean['city'] = df_clean['city'].fillna('Indefinido')
    
    # 5. Remover linhas onde 'ibgeid' é 'nan' (são consolidados estaduais)
    df_clean = df_clean[df_clean['ibgeid'] != 'nan'].copy()

    # (Camada Silver)
    # Salvar em Parquet: formato colunar, muito mais eficiente para análise
    os.makedirs(os.path.dirname(CLEAN_DATA_PATH), exist_ok=True)
    df_clean.to_parquet(CLEAN_DATA_PATH, index=False)
    
    print(f"Dados transformados e salvos com sucesso em: {CLEAN_DATA_PATH}")
    return CLEAN_DATA_PATH

if __name__ == "__main__":
    transform_data(RAW_DATA_PATH)