SELECT
    id_produto,
    nome_produto,
    categoria,
    preco,
    ativo
FROM {{ ref('stg_produtos') }}