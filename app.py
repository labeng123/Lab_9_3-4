from flask import Flask, jsonify, request

app = Flask(__name__)

# Banco de dados em memória simulando a busca e alocação de livrarias
livrarias_mock = {
    1: {"id": 1, "nome": "Livraria Central", "status_alocacao": "disponivel"},
    2: {"id": 2, "nome": "Livraria do Campus", "status_alocacao": "lotada"}
}


# 1. Rota Root (Mantida conforme definido antes)
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "online",
        "mensagem": "Hello World"
    }), 200


# 2. CREATE (POST) - Adicionar uma nova livraria
@app.route('/api/livrarias', methods=['POST'])
def criar_livraria():
    dados = request.get_json()
    if not dados or 'nome' not in dados:
        return jsonify({"erro": "O campo 'nome' eh obrigatorio"}), 400

    novo_id = max(livrarias_mock.keys()) + 1 if livrarias_mock else 1
    nova_livraria = {
        "id": novo_id,
        "nome": dados['nome'],
        "status_alocacao": dados.get('status_alocacao', 'disponivel')
    }

    livrarias_mock[novo_id] = nova_livraria
    return jsonify({"mensagem": "Livraria registrada com sucesso", "dados": nova_livraria}), 201


# 3. READ (GET) - Listar todas as livrarias
@app.route('/api/Buscarlivrarias', methods=['GET'])
def listar_livrarias():
    return jsonify(list(livrarias_mock.values())), 200


# 4. READ (GET) - Buscar uma livraria especifica pelo ID
@app.route('/api/livrarias/<int:livraria_id>', methods=['GET'])
def buscar_livraria(livraria_id):
    livraria = livrarias_mock.get(livraria_id)
    if not livraria:
        return jsonify({"erro": "Livraria nao encontrada"}), 404
    return jsonify(livraria), 200


# 5. UPDATE (PUT) - Atualizar os dados de uma livraria existente
@app.route('/api/livrarias/<int:livraria_id>', methods=['PUT'])
def atualizar_livraria(livraria_id):
    livraria = livrarias_mock.get(livraria_id)
    if not livraria:
        return jsonify({"erro": "Livraria nao encontrada para atualizacao"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado fornecido"}), 400

    livraria['nome'] = dados.get('nome', livraria['nome'])
    livraria['status_alocacao'] = dados.get('status_alocacao', livraria['status_alocacao'])

    return jsonify({"mensagem": "Livraria atualizada com sucesso", "dados": livraria}), 200


# 6. DELETE - Remover uma livraria do sistema
@app.route('/api/livrarias/<int:livraria_id>', methods=['DELETE'])
def deletar_livraria(livraria_id):
    if livraria_id in livrarias_mock:
        del livrarias_mock[livraria_id]
        return jsonify({"mensagem": "Livraria removida com sucesso"}), 200
    return jsonify({"erro": "Livraria nao encontrada"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)