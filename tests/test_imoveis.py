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