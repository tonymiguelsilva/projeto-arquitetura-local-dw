SELECT
    id_produto,
    nome_produto,
    categoria,
    preco
FROM {{ ref('dim_produtos') }}
WHERE ativo = TRUE
