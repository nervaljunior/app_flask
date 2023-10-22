from App import app
from flask import render_template
from flask import request, jsonify
from App.models import db, Usuario, Dado



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/servicos')
def servicos():
    return render_template('servicos.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

from datetime import datetime
from typing import List


# Autenticação de usuário
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Rota para registro de usuário
@app.post("/register", response_model=User)
async def register(user: User):
    try:
        # Verifique se o usuário já existe
        existing_user = await db.users.find_one({"username": user.username})
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        # Insira o novo usuário no banco de dados
        user_data = user.dict()
        user_data["password"] = user.get_password_hash(user_data["password"])
        result = await db.users.insert_one(user_data)

        return {**user.dict(), "id": result.inserted_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rota para fazer login
@app.post("/login", response_model=User)
async def login(user: User):
    try:
        stored_user = await db.users.find_one({"username": user.username})
        if not stored_user:
            raise HTTPException(status_code=400, detail="User not found")
        
        if not user.verify_password(user.password, stored_user["password"]):
            raise HTTPException(status_code=400, detail="Incorrect password")
        
        return user

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rota para obter dados do Arduino
@app.get("/arduino-data", response_model=List[ArduinoData])
async def get_arduino_data():
    try:
        arduino_data = await db.arduino_data.find().to_list(1000)
        return arduino_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create (Criação) - Criar um novo usuário
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    novo_usuario = Usuario(nome=dados['nome'], funcao=dados['funcao'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário criado com sucesso'})

# Read (Leitura) - Recuperar informações de um usuário específico
@app.route('/usuarios/<int:usuario_id>', methods=['GET'])
def obter_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        return jsonify({
            'id': usuario.id,
            'nome': usuario.nome,
            'funcao': usuario.funcao
        })
    return jsonify({'mensagem': 'Usuário não encontrado'}), 404

# Update (Atualização) - Atualizar informações de um usuário existente
@app.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    
    dados = request.get_json()
    usuario.nome = dados['nome']
    usuario.funcao = dados['funcao']
    db.session.commit()
    return jsonify({'mensagem': 'Usuário atualizado com sucesso'})

# Delete (Remoção) - Deletar um usuário existente
@app.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def deletar_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário removido com sucesso'})


@app.route('/dados', methods=['POST'])
def criar_dado():
    dados = request.get_json()
    novo_dado = Dado(data=dados['data'], hora=dados['hora'], intervalo=dados['intervalo'], dados_json=dados['dados_json'],
                     usuario_id=dados['usuario_id'], equipamento_id=dados['equipamento_id'])
    db.session.add(novo_dado)
    db.session.commit()
    return jsonify({'mensagem': 'Dado criado com sucesso'})

