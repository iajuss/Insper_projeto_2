import pytest

from app import app


@pytest.fixture
def client():
    app.config.update(
        TESTING=True,
        DATABASE_NAME="imoveis_test",
    )
    return app.test_client()


def test_listar_imoveis_retorna_imoveis_com_todos_os_atributos(client):
    resposta = client.get("/imoveis")

    assert resposta.status_code == 200
    assert resposta.is_json

    dados = resposta.get_json()

    assert isinstance(dados, dict)
    assert "imoveis" in dados
    assert len(dados["imoveis"]) > 0

    imovel = dados["imoveis"][0]
    campos_esperados = {
        "id",
        "logradouro",
        "tipo_logradouro",
        "bairro",
        "cidade",
        "cep",
        "tipo",
        "valor",
        "data_aquisicao",
    }

    assert campos_esperados <= imovel.keys()

def test_listar_imoveis_informa_link_para_a_propria_colecao(client):
    resposta = client.get("/imoveis")

    dados = resposta.get_json()

    assert "_links" in dados
    assert dados["_links"]["self"] == {
        "href": "/imoveis",
        "method": "GET",
    }


def test_lista_imovel_pelo_id(client):
    resposta_lista = client.get("/imoveis")

    assert resposta_lista.status_code == 200

    dados_lista = resposta_lista.get_json()
    imovel_listado = dados_lista["imoveis"][0]
    imovel_id = imovel_listado["id"]

    resposta = client.get(f"/imoveis/{imovel_id}")

    assert resposta.status_code == 200
    assert resposta.is_json

    dados = resposta.get_json()

    assert isinstance(dados, dict)
    assert "imovel" in dados

    imovel = dados["imovel"]
    campos_esperados = {
        "id",
        "logradouro",
        "tipo_logradouro",
        "bairro",
        "cidade",
        "cep",
        "tipo",
        "valor",
        "data_aquisicao",
    }

    assert campos_esperados <= imovel.keys()
    assert imovel["id"] == imovel_id

def test_criar_novo_imovel(client):
    novo_imovel = {
        "logradouro": "Rua das Flores",
        "tipo_logradouro": "Rua",
        "bairro": "Centro",
        "cidade": "Sao Paulo",
        "cep": "01234-567",
        "tipo": "Apartamento",
        "valor": 500000.00,
        "data_aquisicao": "2024-05-10",
    }

    resposta = client.post("/imoveis", json=novo_imovel)

    assert resposta.status_code == 201
    assert resposta.is_json

    dados = resposta.get_json()

    assert isinstance(dados, dict)
    assert "imovel" in dados

    imovel = dados["imovel"]

    assert "id" in imovel
    assert imovel["id"] is not None

    assert imovel["logradouro"] == novo_imovel["logradouro"]
    assert imovel["tipo_logradouro"] == novo_imovel["tipo_logradouro"]
    assert imovel["bairro"] == novo_imovel["bairro"]
    assert imovel["cidade"] == novo_imovel["cidade"]
    assert imovel["cep"] == novo_imovel["cep"]
    assert imovel["tipo"] == novo_imovel["tipo"]
    assert imovel["valor"] == novo_imovel["valor"]
    assert imovel["data_aquisicao"] == novo_imovel["data_aquisicao"]

def test_atualiza_funcao(client):

    resposta_lista = client.get("/imoveis")

    assert resposta_lista.status_code == 200

    dados_lista = resposta_lista.get_json()
    imovel_id = dados_lista["imoveis"][0]["id"]

    imovel_atualizado = {
        "logradouro": "Avenida Paulista",
        "tipo_logradouro": "Avenida",
        "bairro": "Bela Vista",
        "cidade": "Sao Paulo",
        "cep": "01310-100",
        "tipo": "Comercial",
        "valor": 750000.00,
        "data_aquisicao": "2025-01-15",
    }

    resposta = client.put(f"/imoveis/{imovel_id}", json=imovel_atualizado)

    assert resposta.status_code == 200
    assert resposta.is_json

    dados = resposta.get_json()

    assert "imovel" in dados

    imovel = dados["imovel"]

    assert imovel["id"] == imovel_id
    assert imovel["logradouro"] == imovel_atualizado["logradouro"]
    assert imovel["tipo_logradouro"] == imovel_atualizado["tipo_logradouro"]
    assert imovel["bairro"] == imovel_atualizado["bairro"]
    assert imovel["cidade"] == imovel_atualizado["cidade"]
    assert imovel["cep"] == imovel_atualizado["cep"]
    assert imovel["tipo"] == imovel_atualizado["tipo"]
    assert imovel["valor"] == imovel_atualizado["valor"]
    assert imovel["data_aquisicao"] == imovel_atualizado["data_aquisicao"]

def test_listar_imoveis_informa_como_criar_um_imovel(client):
    resposta = client.get("/imoveis")

    dados = resposta.get_json()

    assert "create" in dados["_links"]
    assert dados["_links"]["create"] == {
        "href": "/imoveis",
        "method": "POST",
    }

def test_listar_imovel_por_id_informa_link_para_si_mesmo(client):
    resposta_lista = client.get("/imoveis")
    imovel_id = resposta_lista.get_json()["imoveis"][0]["id"]

    resposta = client.get(f"/imoveis/{imovel_id}")
    dados = resposta.get_json()

    assert "_links" in dados
    assert dados["_links"]["self"] == {
        "href": f"/imoveis/{imovel_id}",
        "method": "GET",
    }

def test_listar_imovel_por_id_informa_link_para_a_colecao(client):
    resposta_lista = client.get("/imoveis")
    imovel_id = resposta_lista.get_json()["imoveis"][0]["id"]

    resposta = client.get(f"/imoveis/{imovel_id}")
    dados = resposta.get_json()

    assert "collection" in dados["_links"]
    assert dados["_links"]["collection"] == {
        "href": "/imoveis",
        "method": "GET",
    }

def test_remover_imovel(client):
    novo_imovel = {
        "logradouro": "Rua do Teste de Remocao",
        "tipo_logradouro": "Rua",
        "bairro": "Centro",
        "cidade": "Sao Paulo",
        "cep": "01000-000",
        "tipo": "Casa",
        "valor": 300000.00,
        "data_aquisicao": "2025-01-01",
    }

    resposta_criacao = client.post("/imoveis", json=novo_imovel)
    imovel_id = resposta_criacao.get_json()["imovel"]["id"]

    resposta_remocao = client.delete(f"/imoveis/{imovel_id}")

    assert resposta_remocao.status_code == 204
    assert resposta_remocao.data == b""

    resposta_consulta = client.get(f"/imoveis/{imovel_id}")
    assert resposta_consulta.status_code == 404