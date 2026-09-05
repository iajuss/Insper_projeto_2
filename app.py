from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/imoveis")
def listar_imoveis():
    return jsonify([]), 200