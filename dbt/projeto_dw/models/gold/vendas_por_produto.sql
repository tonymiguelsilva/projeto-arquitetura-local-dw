{{ config(materialized='table') }}

SELECT
    p.id_produto,
    p.nome_produto,
    p.categoria,
    SUM(v.quantidade) AS quantidade_vendida,
    SUM(v.valor_total) AS faturamento_total,
    AVG(v.valor_total) AS ticket_medio
FROM {{ ref('fato_vendas') }} v
INNER JOIN {{ ref('dim_produtos') }} p
    ON v.id_produto = p.id_produto
GROUP BY
    p.id_produto,
    p.nome_produto,
    p.categoria