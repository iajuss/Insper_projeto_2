import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_listar_imoveis(client):
    resposta = client.get("/imoveis")

    assert resposta.status_code == 200