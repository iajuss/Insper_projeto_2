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

## Rotas da API

| Método | Rota | Descrição | Respostas esperadas |
| --- | --- | --- | --- |
| `GET` | `/imoveis` | Lista todos os imóveis. | `200 OK` |
| `GET` | `/imoveis/<id>` | Consulta um imóvel pelo identificador. | `200 OK`, `404 Not Found` |
| `POST` | `/imoveis` | Cria um imóvel com todos os atributos obrigatórios. | `201 Created`, `400 Bad Request` |
| `PUT` | `/imoveis/<id>` | Atualiza um imóvel existente. | `200 OK`, `400 Bad Request`, `404 Not Found` |
| `DELETE` | `/imoveis/<id>` | Remove um imóvel existente. | `204 No Content`, `404 Not Found` |
| `GET` | `/imoveis?tipo=<tipo>` | Filtra imóveis por tipo. | `200 OK` |
| `GET` | `/imoveis?cidade=<cidade>` | Filtra imóveis por cidade. | `200 OK` |
| `GET` | `/imoveis?tipo=<tipo>&cidade=<cidade>` | Combina os filtros de tipo e cidade. | `200 OK` |
| `GET` | `/imoveis/tipo/<tipo>` | Busca imóveis por tipo por meio de rota alternativa. | `200 OK` |
| `GET` | `/imoveis/cidade/<cidade>` | Busca imóveis por cidade por meio de rota alternativa. | `200 OK` |

Uma busca sem resultados é válida e retorna `200 OK` com a lista `imoveis` vazia.

## Hipermídia

As respostas utilizam o campo `_links` para informar ações e navegação disponíveis. Por exemplo, um imóvel individual pode informar links para consultá-lo (`self`), voltar à coleção (`collection`), atualizá-lo (`update`) ou removê-lo (`delete`).

Na criação de um imóvel, a API retorna `201 Created`, o cabeçalho HTTP `Location` e um link `self` para o recurso recém-criado.
