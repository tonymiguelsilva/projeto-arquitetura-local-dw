from datetime import datetime, timedelta

import requests
import psycopg2

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.email import send_email


def enviar_email_falha(context):
    task = context["task_instance"]

    send_email(
        to=[Variable.get("ALERT_EMAIL")],
        subject=f"❌ Falha na DAG: {task.dag_id}",
        html_content=f"""
        <h2>Falha no pipeline</h2>

        <p><strong>DAG:</strong> {task.dag_id}</p>
        <p><strong>Task:</strong> {task.task_id}</p>
        <p><strong>Execução:</strong> {context.get("run_id")}</p>
        <p><strong>Log:</strong>
        <a href="{task.log_url}">Abrir log no Airflow</a>
        </p>
        """,
    )

def enviar_email_sucesso(context):
    send_email(
        to=[Variable.get("ALERT_EMAIL")],
        subject=f"✅ DAG concluída: {context['dag'].dag_id}",
        html_content=f"""
        <h2>Pipeline concluído com sucesso</h2>
        <p><strong>DAG:</strong> {context['dag'].dag_id}</p>
        <p><strong>Execução:</strong> {context.get("run_id")}</p>
        """,
    )


default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


def extrair_clientes():

    response = requests.get(
        "http://projeto_dw_api:8000/clientes",
        timeout=30,
    )

    response.raise_for_status()

    clientes = response.json()

    print(f"Clientes extraídos da API: {len(clientes)}")

    conn = psycopg2.connect(
        host="postgres_dw",
        port=5432,
        user="dw_user",
        password="dw_password",
        dbname="dw",
    )

    cur = conn.cursor()

    cur.execute("TRUNCATE TABLE origem_clientes")

    for cliente in clientes:
        cur.execute(
            """
            INSERT INTO origem_clientes (
                id_cliente,
                nome_cliente,
                cidade,
                estado,
                data_cadastro,
                ativo
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                cliente["id_cliente"],
                cliente["nome_cliente"],
                cliente["cidade"],
                cliente["estado"],
                None,
                cliente["ativo"],
            ),
        )

    conn.commit()

    cur.close()
    conn.close()

    print("Carga de clientes concluída!")


def extrair_produtos():

    response = requests.get(
        "http://projeto_dw_api:8000/produtos",
        timeout=30,
    )

    response.raise_for_status()

    produtos = response.json()

    print(f"Produtos extraídos da API: {len(produtos)}")

    conn = psycopg2.connect(
        host="postgres_dw",
        port=5432,
        user="dw_user",
        password="dw_password",
        dbname="dw",
    )

    cur = conn.cursor()

    cur.execute("TRUNCATE TABLE origem_produtos")

    for produto in produtos:
        cur.execute(
            """
            INSERT INTO origem_produtos (
                id_produto,
                nome_produto,
                categoria,
                preco,
                ativo
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                produto["id_produto"],
                produto["nome_produto"],
                produto["categoria"],
                produto["preco"],
                produto["ativo"],
            ),
        )

    conn.commit()

    cur.close()
    conn.close()

    print("Carga de produtos concluída!")


def extrair_vendas():

    oltp = psycopg2.connect(
        host="projeto_oltp_postgres",
        port=5432,
        user="oltp_user",
        password="oltp_password",
        dbname="oltp",
    )

    dw = psycopg2.connect(
        host="postgres_dw",
        port=5432,
        user="dw_user",
        password="dw_password",
        dbname="dw",
    )

    oltp_cur = oltp.cursor()
    dw_cur = dw.cursor()

    oltp_cur.execute(
        """
        SELECT
            id_venda,
            id_cliente,
            id_produto,
            data_venda,
            quantidade,
            valor_unitario
        FROM vendas
        """
    )

    vendas = oltp_cur.fetchall()

    print(f"Vendas extraídas do OLTP: {len(vendas)}")

    dw_cur.execute("TRUNCATE TABLE origem_vendas")

    for venda in vendas:
        dw_cur.execute(
            """
            INSERT INTO origem_vendas (
                id_venda,
                id_cliente,
                id_produto,
                data_venda,
                quantidade,
                valor_unitario
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            venda,
        )

    dw.commit()

    oltp_cur.close()
    dw_cur.close()

    oltp.close()
    dw.close()

    print("Carga de vendas concluída!")


with DAG(
    dag_id="dw_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    default_args=default_args,
    on_failure_callback=enviar_email_falha,
    on_success_callback=enviar_email_sucesso,
    tags=["dw", "etl", "dbt"],
) as dag:

    carga_clientes = PythonOperator(
        task_id="carga_clientes",
        python_callable=extrair_clientes,
    )

    carga_produtos = PythonOperator(
        task_id="carga_produtos",
        python_callable=extrair_produtos,
    )

    carga_vendas = PythonOperator(
        task_id="carga_vendas",
        python_callable=extrair_vendas,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="""
            cd /usr/local/airflow/dbt/projeto_dw &&
            dbt run --target prod
        """,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="""
            cd /usr/local/airflow/dbt/projeto_dw &&
            dbt test
        """,
    )

    [
        carga_clientes,
        carga_produtos,
        carga_vendas,
    ] >> dbt_run >> dbt_test