{{ config(materialized='table') }}

SELECT
    COUNT(*) AS total_vendas,
    SUM(quantidade) AS total_itens,
    SUM(valor_total) AS faturamento_total,
    AVG(valor_total) AS ticket_medio
FROM {{ ref('fato_vendas') }}