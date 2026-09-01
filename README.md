# Arquitetura Local de Data Warehouse

Projeto de Engenharia de Dados desenvolvido para estudar e aplicar uma arquitetura de Data Warehouse em ambiente local, utilizando Docker, Apache Airflow, PostgreSQL, dbt e uma API REST.

## Arquitetura

```text
API REST
   ↓
Apache Airflow
   ↓
PostgreSQL
   ↓
dbt
   ↓
Bronze → Silver → Gold
   ↓
Power BI
```

O projeto possui ambientes separados de desenvolvimento e produção no dbt.

## Tecnologias

* Python
* FastAPI
* Apache Airflow
* PostgreSQL
* dbt Core
* Docker
* DBeaver
* Power BI
* Git

## Pipeline

A DAG `dw_pipeline` realiza a ingestão de clientes, produtos e vendas a partir da API REST e carrega os dados no PostgreSQL.

Após a ingestão, o Airflow executa o dbt para transformação e validação dos dados.

```text
Extração → PostgreSQL → dbt run → dbt test
```

A DAG possui retries, tratamento de falhas e notificações por e-mail.

## Modelagem

O dbt organiza os modelos em três camadas.

### Bronze

Dados preparados a partir das fontes:

* `stg_clientes`
* `stg_produtos`
* `stg_vendas`

### Silver

Modelagem dos dados para utilização no Data Warehouse:

* `dim_clientes`
* `dim_produtos`
* `fato_vendas`

### Gold

Modelos preparados para consumo analítico:

* `clientes_ativos`
* `produtos_ativos`
* `resumo_clientes`
* `resumo_vendas`
* `vendas_por_cliente`
* `vendas_por_produto`

## Ambientes

O dbt possui targets separados para desenvolvimento e produção.

```text
DEV
dbt_dev_bronze
dbt_dev_silver
dbt_dev_gold

PROD
dbt_prod_bronze
dbt_prod_silver
dbt_prod_gold
```

A pipeline do Airflow executa o ambiente PROD.

## Qualidade dos dados

O projeto possui testes automatizados utilizando dbt, incluindo validações de `not_null` e `unique`.

Atualmente são executados 14 testes de dados no ambiente PROD.

```text
PASS=14
WARN=0
ERROR=0
```

## Consumo

O PostgreSQL funciona como Data Warehouse central do projeto.

O DBeaver é utilizado para exploração e administração do banco, enquanto o Power BI está conectado à camada `dbt_prod_gold`.

## Estrutura

```text
projeto_arquitetura_dw/
│
├── api/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── dags/
│   ├── dw_pipeline.py
│   └── .airflowignore
│
├── dbt/
│   └── projeto_dw/
│       ├── models/
│       │   ├── bronze/
│       │   ├── silver/
│       │   └── gold/
│       ├── dbt_project.yml
│       └── profiles.yml
│
├── docker-compose.dw.yml
├── docker-compose.override.yml
├── Dockerfile
└── requirements.txt
```

## Como executar e testar

### Pré-requisitos

* Docker Desktop
* Git
* Astro CLI

### Inicialização

Clone o repositório e entre na pasta do projeto.

Configure as variáveis de ambiente no arquivo `.env` e inicie o ambiente:

```bash
astro dev start
```

O Airflow estará disponível em:

```text
http://localhost:8080
```

### Executando o pipeline

No Airflow, execute a DAG:

```text
dw_pipeline
```

O fluxo executado é:

```text
API
 ↓
PostgreSQL
 ↓
dbt run
 ↓
dbt test
```

Para executar o dbt manualmente:

```bash
astro dev bash

cd /usr/local/airflow/dbt/projeto_dw

dbt run --target prod
dbt test --target prod
```

Os dados transformados podem ser consultados no PostgreSQL através do DBeaver, principalmente no schema:

```text
dbt_prod_gold
```

## Objetivo

Aplicar conceitos de Engenharia de Dados em um projeto completo, incluindo ingestão, orquestração, Data Warehouse, modelagem dimensional, transformação com dbt, testes de qualidade, containerização e integração com ferramentas de Analytics.
