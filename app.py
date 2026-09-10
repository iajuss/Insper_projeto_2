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
    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute(
            """
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
        )
        imoveis = cursor.fetchall()
    finally:
        cursor.close()
        conexao.close()

    return jsonify({"imoveis": imoveis}), 200


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

    return jsonify({'imovel':imovel}), 200

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