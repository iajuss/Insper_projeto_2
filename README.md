# Insper_projeto_2

## Sobre o projeto

API RESTful para gerenciamento de imóveis, desenvolvida com Flask e MySQL hospedado no Aiven.

## Tecnologias

- Python
- Flask
- MySQL
- Aiven
- Pytest

## Configuração local

Crie um arquivo `.env` na raiz do projeto com:

```env
DB_HOST=host-do-aiven
DB_PORT=porta-do-aiven
DB_USER=usuario-do-aiven
DB_PASSWORD=senha-do-aiven
DB_NAME=imoveis_app
TEST_DB_NAME=imoveis_test
DB_SSL_CA=caminho-para-ca.pem
```

Não envie o arquivo `.env` nem `ca.pem` ao repositório.

## Como executar

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
flask --app app run
```

## Como executar os testes

```powershell
python -m pytest -v
```
