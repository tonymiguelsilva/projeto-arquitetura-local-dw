from fastapi import FastAPI

app = FastAPI(title="API de Clientes")


@app.get("/clientes")
def listar_clientes():
    return [
        {
            "id_cliente": 1,
            "nome_cliente": "Joao Silva",
            "cidade": "Novo Hamburgo",
            "estado": "RS",
            "ativo": True
        },
        {
            "id_cliente": 2,
            "nome_cliente": "Maria Souza",
            "cidade": "Porto Alegre",
            "estado": "RS",
            "ativo": True
        },
        {
            "id_cliente": 3,
            "nome_cliente": "Carlos Oliveira",
            "cidade": "Sao Leopoldo",
            "estado": "RS",
            "ativo": False
        },
        {
            "id_cliente": 4,
            "nome_cliente": "Ana Santos",
            "cidade": "Canoas",
            "estado": "RS",
            "ativo": True
        },
        {
            "id_cliente": 5,
            "nome_cliente": "Pedro Costa",
            "cidade": "Gravatai",
            "estado": "RS",
            "ativo": True
        },
	        {
            "id_cliente": 6,
            "nome_cliente": "Lucas Pereira",
            "cidade": "Portao",
            "estado": "RS",
            "ativo": True
        }
    ]

@app.get("/produtos")
def listar_produtos():
    return [
        {
            "id_produto": 1,
            "nome_produto": "Notebook",
            "categoria": "Eletronicos",
            "preco": 3500.00,
            "ativo": True
        },
        {
            "id_produto": 2,
            "nome_produto": "Monitor",
            "categoria": "Eletronicos",
            "preco": 1200.00,
            "ativo": True
        },
        {
            "id_produto": 3,
            "nome_produto": "Teclado",
            "categoria": "Perifericos",
            "preco": 250.00,
            "ativo": True
        },
        {
            "id_produto": 4,
            "nome_produto": "Mouse",
            "categoria": "Perifericos",
            "preco": 150.00,
            "ativo": True
        },
        {
            "id_produto": 5,
            "nome_produto": "Cadeira",
            "categoria": "Moveis",
            "preco": 900.00,
            "ativo": True
        }
    ]