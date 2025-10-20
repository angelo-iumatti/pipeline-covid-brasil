# Pipeline de Dados: Análise de Casos de COVID-19 no Brasil

Este projeto é um pipeline de ETL (Extract, Transform, Load) de nível iniciante, 
desenvolvido como parte do meu portfólio de Engenharia de Dados. 

O objetivo é ingerir dados públicos de COVID-19, transformá-los e carregá-los 
em um banco de dados analítico (DuckDB) pronto para consultas.

## 🎯 Objetivo

Demonstrar as competências fundamentais da Engenharia de Dados:
- **Extração:** Coleta de dados de uma fonte externa (API/Web).
- **Transformação:** Limpeza, normalização e modelagem dos dados (Camadas Bronze -> Silver -> Gold).
- **Carga:** Armazenamento dos dados em um Data Warehouse/DB analítico.
- **Automação:** Orquestração do pipeline usando CI/CD (GitHub Actions).

## 🏛️ Arquitetura do Pipeline

1.  **Extração:** Um script Python (`requests`) busca o CSV de casos do repositório de Wesley Cota (fonte: Min. Saúde).
2.  **Transformação:** Os dados brutos (CSV) são limpos usando `pandas` e salvos em formato `Parquet` (Camada Silver).
3.  **Carga:** O `DuckDB` é usado para ler o Parquet e criar duas tabelas (Camada Gold):
    - `cases_covid_brasil`: Dados limpos e detalhados por município.
    - `daily_summary_brasil`: Dados agregados (total de casos/mortes por dia no país).
4.  **Orquestração:** O GitHub Actions executa o pipeline (`main.py`) automaticamente via agendamento (CRON) ou em cada push para a branch `main`.

## 🚀 Tecnologias Utilizadas

- **Linguagem:** Python 3.10
- **Bibliotecas:** Pandas, Requests
- **Banco de Dados:** DuckDB (Data Warehouse analítico "in-process")
- **Orquestração/CI/CD:** GitHub Actions
- **Formato de Dados:** CSV (Bronze), Parquet (Silver)

## ⚙️ Como Executar Localmente

1.  Clone este repositório:
    ```bash
    git clone [https://github.com/SEU-USUARIO/pipeline-covid-brasil.git](https://github.com/SEU-USUARIO/pipeline-covid-brasil.git)
    cd pipeline-covid-brasil
    ```

2.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4.  Execute o pipeline principal:
    ```bash
    python src/main.py
    ```

5.  (Opcional) Para consultar os dados gerados:
    ```bash
    # Instale o DuckDB CLI (se desejar)
    pip install duckdb-cli
    # Abra o banco de dados
    duckdb data/covid_analytics.db
    # Rode uma consulta SQL
    duckdb> SELECT * FROM daily_summary_brasil LIMIT 10;
    ```