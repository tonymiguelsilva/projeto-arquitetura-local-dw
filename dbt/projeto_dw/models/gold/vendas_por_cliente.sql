{{ config(materialized='table') }}

SELECT
    c.id_cliente,
    c.nome_cliente,
    c.cidade,
    c.estado,
    COUNT(v.id_venda) AS total_vendas,
    SUM(v.quantidade) AS quantidade_comprada,
    SUM(v.valor_total) AS faturamento_total,
    AVG(v.valor_total) AS ticket_medio
FROM {{ ref('fato_vendas') }} v
INNER JOIN {{ ref('dim_clientes') }} c
    ON v.id_cliente = c.id_cliente
GROUP BY
    c.id_cliente,
    c.nome_cliente,
    c.cidade,
    c.estado