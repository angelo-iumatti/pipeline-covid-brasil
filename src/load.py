import duckdb
import os

CLEAN_DATA_PATH = os.path.join("data", "clean_cases_covid.parquet")
DB_PATH = os.path.join("data", "covid_analytics.db")

def load_data_to_duckdb(clean_path):
    """
    Carrega os dados limpos (Parquet) para uma tabela no DuckDB.
    """
    print(f"Iniciando carga para o DuckDB: {DB_PATH}")

    if not os.path.exists(clean_path):
        print(f"Arquivo de dados limpos não encontrado: {clean_path}")
        return

    # Conectar ao DuckDB (ele cria o arquivo .db se não existir)
    con = duckdb.connect(database=DB_PATH, read_only=False)
    
    # Criar uma tabela (ou substituir se já existir)
    # O DuckDB pode ler Parquet diretamente! Isso é muito poderoso.
    try:
        con.execute(f"""
            CREATE OR REPLACE TABLE cases_covid_brasil AS 
            SELECT * FROM read_parquet('{clean_path}');
        """)
        
        print("Tabela 'cases_covid_brasil' criada/atualizada com sucesso.")
        
        # Bônus: Criar uma tabela agregada (Camada Gold)
        con.execute("""
            CREATE OR REPLACE TABLE daily_summary_brasil AS
            SELECT
                date,
                SUM(totalcases) AS total_cases_pais,
                SUM(deaths) AS total_deaths_pais
            FROM cases_covid_brasil
            GROUP BY date
            ORDER BY date;
        """)
        print("Tabela agregada 'daily_summary_brasil' criada/atualizada.")

    except Exception as e:
        print(f"Erro ao carregar dados no DuckDB: {e}")
    finally:
        con.close()

if __name__ == "__main__":
    load_data_to_duckdb(CLEAN_DATA_PATH)