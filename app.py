import os

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, jsonify, request


load_dotenv()

app = Flask(__name__)

app.config.from_mapping(
    DB_HOST=os.getenv("DB_HOST"),
    DB_PORT=int(os.getenv("DB_PORT", "3306")),
    DB_USER=os.getenv("DB_USER"),
    DB_PASSWORD=os.getenv("DB_PASSWORD"),
    DATABASE_NAME=os.getenv("DB_NAME"),
    DB_SSL_CA=os.getenv("DB_SSL_CA"),
)


def criar_conexao():
    return mysql.connector.connect(
        host=app.config["DB_HOST"],
        port=app.config["DB_PORT"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        database=app.config["DATABASE_NAME"],
        ssl_ca=app.config["DB_SSL_CA"],
        ssl_verify_cert=True,
    )


@app.get("/imoveis")
def listar_imoveis():
    tipo = request.args.get("tipo")
    cidade = request.args.get("cidade")

    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    try:
        consulta = """
            SELECT
                id,
                logradouro,
                tipo_logradouro,
                bairro,
                cidade,
                cep,
                tipo,
                valor,
                data_aquisicao
            FROM imoveis
        """

        condicoes = []
        parametros = []

        if tipo is not None:
            condicoes.append("tipo = %s")
            parametros.append(tipo)

        if cidade is not None:
            condicoes.append("cidade = %s")
            parametros.append(cidade)

        if condicoes:
            consulta += " WHERE " + " AND ".join(condicoes)

        cursor.execute(consulta, tuple(parametros))
        imoveis = cursor.fetchall()
    finally:
        cursor.close()
        conexao.close()

    return jsonify({
        "imoveis": imoveis,
        "_links": {
            "self": {
                "href": "/imoveis",
                "method": "GET",
            },
            "create": {
                "href": "/imoveis",
                "method": "POST",
            },
        },
    }), 200

@app.get("/imoveis/<int:imovel_id>")
def listar_imovel_pelo_id(imovel_id):
    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute('SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis WHERE id = %s', (imovel_id,))

    imovel = cursor.fetchone()

    if imovel is None:
        return jsonify({"erro": "Imovel nao encontrado"}), 404

    cursor.close()
    conexao.close()

    return jsonify({
    "imovel": imovel,
    "_links": {
        "self": {
            "href": f"/imoveis/{imovel_id}",
            "method": "GET",
        },
        "collection": {
            "href": "/imoveis",
            "method": "GET",
        },
        "delete": {
            "href": f"/imoveis/{imovel_id}",
            "method": "DELETE",
        },
        "update": {
            "href": f"/imoveis/{imovel_id}",
            "method": "PUT",
        },
                },
    }), 200

@app.route("/imoveis", methods=['POST'])
def cria_novo_imovel():
    imovel = request.get_json()

    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (imovel['logradouro'], imovel['tipo_logradouro'], imovel['bairro'], imovel['cidade'], imovel['cep'], imovel['tipo'], imovel['valor'], imovel['data_aquisicao']))

    conexao.commit()

    imovel['id'] = cursor.lastrowid

    cursor.close()
    conexao.close()

    return jsonify({'imovel': imovel}), 201

@app.route('/imoveis/<int:id>', methods=['PUT'])
def atualiza_imovel(id):
    imovel = request.get_json()

    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute('UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s', (imovel['logradouro'], imovel['tipo_logradouro'], imovel['bairro'], imovel['cidade'], imovel['cep'], imovel['tipo'], imovel['valor'], imovel['data_aquisicao'], id))

    conexao.commit()

    imovel['id'] = id

    cursor.close()
    conexao.close()

    return jsonify({'imovel': imovel}), 200

@app.delete("/imoveis/<int:imovel_id>")
def remover_imovel(imovel_id):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            "DELETE FROM imoveis WHERE id = %s",
            (imovel_id,),
        )

        if cursor.rowcount == 0:
            return jsonify({"erro": "Imovel nao encontrado"}), 404

        conexao.commit()
        return "", 204
    finally:
        cursor.close()
        conexao.close()