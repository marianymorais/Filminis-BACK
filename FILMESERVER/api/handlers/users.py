import os
import json, hashlib, time
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from infra.database import *
from infra.users_database import *
from infra.actorsDirectors import *
from infra.genresProducers import *
from api.jwt import *


def get_Me(handler):
    header_auth = handler.headers.get("Authorization", "")

    if not header_auth.startswith("Bearer "):
        handler._send_json({"error": "Token não informado"}, 401)
        return

    token = header_auth.split(" ")[1]
    payload = verify_jwt(token)

    if not payload:
        handler._send_json({"error": "Token inválido ou expirado"}, 401)
        return

    email = payload.get("sub")

    user = getUserByEmail(email)

    if not user:
        handler._send_json({"error": "Usuário não encontrado"}, 404)
        return

    user.pop("senha", None)

    if user.get("data_criacao"):
        user["data_criacao"] = str(user["data_criacao"])

    if user.get("data_nascimento"):
        user["data_nascimento"] = str(user["data_nascimento"])

    handler._send_json(user)

def get_Usuarios(handler):
    header_auth = handler.headers.get("Authorization", "")

    if not header_auth.startswith("Bearer "):
        handler._send_json({"error": "Token não informado"}, 401)
        return

    token = header_auth.split(" ")[1]
    payload = verify_jwt(token)

    if not payload or payload.get("role") != "admin":
        handler._send_json({"error": "Apenas admin pode listar usuários"}, 403)
        return

    usuarios = getUsuarios()

    usuarios = serializeUsuarios(usuarios)

    handler._send_json(usuarios)

def post_Register(handler):
    content_length = int(handler.headers['Content-Length'])
    body = handler.rfile.read(content_length).decode('utf-8')

    try:
        data = json.loads(body)
    except:
        handler._send_json({"error": "JSON inválido"}, 400)
        return

    nome = data.get("nome")
    sobrenome = data.get("sobrenome")
    apelido = data.get("apelido")
    email = data.get("email")
    senha = data.get("senha")
    data_nascimento = data.get("data_nascimento")
    imagem = data.get("imagem")

    if not nome or not email or not senha:
        handler._send_json(
            {"error": "Campos obrigatórios: nome, email e senha"},
            400
        )
        return

    result = insertUser(
        nome=nome,
        sobrenome=sobrenome,
        apelido=apelido,
        email=email,
        senha=senha,
        data_nascimento=data_nascimento,
        imagem=imagem,
        role="user"
    )

    if result:
        handler._send_json(result, 201)
    else:
        handler._send_json({"error": "Erro ao cadastrar usuário"}, 400)

def patch_UsersRole(handler):
    header_auth = handler.headers.get("Authorization", "")

    if not header_auth.startswith("Bearer "):
        handler._send_json({"error": "Token não informado"}, 401)
        return

    token = header_auth.split(" ")[1]
    payload = verify_jwt(token)

    if not payload or payload.get("role") != "admin":
        handler._send_json(
            {"error": "Apenas administradores podem alterar roles"},
            403
        )
        return

    params = parse_qs(urlparse(handler.path).query)
    id_usuario = params.get("id", [None])[0]

    try:
        id_usuario = int(id_usuario)
    except:
        handler._send_json({"error": "ID inválido"}, 400)
        return

    content_length = int(handler.headers.get("Content-Length", 0))
    body = handler.rfile.read(content_length).decode("utf-8")

    try:
        data = json.loads(body)
    except:
        handler._send_json({"error": "JSON inválido"}, 400)
        return

    nova_role = data.get("role")

    if nova_role not in ["admin", "user"]:
        handler._send_json({"error": "Role inválida"}, 400)
        return

    sucesso = atualizarRoleUser(id_usuario, nova_role)

    if sucesso:
        handler._send_json(
            {"message": f"Role do usuário alterada para {nova_role}"}
        )
    else:
        handler._send_json(
            {"error": "Usuário não encontrado"},
            404
        )

def patch_EditMe(handler):
    header_auth = handler.headers.get("Authorization", "")

    if not header_auth.startswith("Bearer "):
        handler._send_json({"error": "Token não informado"}, 401)
        return

    token = header_auth.split(" ")[1]
    payload = verify_jwt(token)

    if not payload:
        handler._send_json({"error": "Token inválido ou expirado"}, 401)
        return

    email = payload.get("sub")

    content_length = int(handler.headers.get("Content-Length", 0))
    body = handler.rfile.read(content_length).decode('utf-8')

    try:
        data = json.loads(body)
    except:
        handler._send_json({"error": "JSON inválido"}, 400)
        return

    campos = {}

    if "nome" in data:
        campos["nome"] = data["nome"]

    if "sobrenome" in data:
        campos["sobrenome"] = data["sobrenome"]

    if "apelido" in data:
        campos["apelido"] = data["apelido"]

    if "data_nascimento" in data:
        campos["data_nascimento"] = data["data_nascimento"]

    if "imagem" in data:
        campos["imagem"] = data["imagem"]

    if not campos:
        handler._send_json({"error": "Nenhum campo para atualizar"}, 400)
        return

    patchUsuario(email, campos)

    handler._send_json({"message": "Perfil atualizado com sucesso"})
