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