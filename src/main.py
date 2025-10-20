from extract import extract_data
from transform import transform_data
from load import load_data_to_duckdb

def run_pipeline():
    """
    Executa o pipeline de ETL completo.
    """
    print("Iniciando o pipeline de ETL de COVID-19...")
    
    # 1. Extração
    raw_path = extract_data()
    if raw_path is None:
        print("Falha na extração. Abortando pipeline.")
        return

    # 2. Transformação
    clean_path = transform_data(raw_path)
    if clean_path is None:
        print("Falha na transformação. Abortando pipeline.")
        return

    # 3. Carga
    load_data_to_duckdb(clean_path)
    
    print("Pipeline de ETL concluído com sucesso!")

if __name__ == "__main__":
    run_pipeline()