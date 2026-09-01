SELECT
    id_produto,
    nome_produto,
    categoria,
    preco,
    ativo
FROM {{ source('postgres_dw', 'origem_produtos') }}