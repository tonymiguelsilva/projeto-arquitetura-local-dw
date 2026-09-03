CREATE TABLE IF NOT EXISTS public.origem_clientes (
    id_cliente INTEGER PRIMARY KEY,
    nome_cliente VARCHAR(150) NOT NULL,
    cidade VARCHAR(100),
    estado CHAR(2),
    data_cadastro TIMESTAMP,
    ativo BOOLEAN
);

CREATE TABLE IF NOT EXISTS public.origem_produtos (
    id_produto INTEGER PRIMARY KEY,
    nome_produto VARCHAR(150) NOT NULL,
    categoria VARCHAR(100),
    preco NUMERIC(12,2),
    ativo BOOLEAN
);

CREATE TABLE IF NOT EXISTS public.origem_vendas (
    id_venda INTEGER PRIMARY KEY,
    id_cliente INTEGER,
    id_produto INTEGER,
    data_venda TIMESTAMP,
    quantidade INTEGER,
    valor_unitario NUMERIC(12,2)
);