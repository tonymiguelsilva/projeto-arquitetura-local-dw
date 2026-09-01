{{ config(
    materialized='incremental',
    unique_key='id_venda'
) }}

SELECT
    v.id_venda,
    v.id_cliente,
    v.id_produto,
    v.data_venda,
    v.quantidade,
    v.valor_unitario,
    v.quantidade * v.valor_unitario AS valor_total

FROM {{ ref('stg_vendas') }} v

{% if is_incremental() %}

WHERE v.id_venda > (
    SELECT COALESCE(MAX(id_venda), 0)
    FROM {{ this }}
)

{% endif %}