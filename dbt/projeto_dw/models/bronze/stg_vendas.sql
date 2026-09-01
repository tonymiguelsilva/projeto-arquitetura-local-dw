select
    id_venda,
    id_cliente,
    id_produto,
    data_venda,
    quantidade,
    valor_unitario
from {{ source('postgres_dw', 'origem_vendas') }}