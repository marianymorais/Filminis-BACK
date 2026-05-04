import os
import json, hashlib, time
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from infra.database import *
from infra.users_database import *
from infra.actorsDirectors import *
from infra.genresProducers import *
from api.jwt import *

def post_Loginho(handler):
    content_length = int(handler.headers['Content-length'])
    body = handler.rfile.read(content_length).decode('utf-8')
    form_data = parse_qs(body)

    email = form_data.get("email", [""])[0]
    password = form_data.get("password", [""])[0]
    hashed = hashlib.sha256(password.encode()).hexdigest()

    print("Data form:")
    print("Email:", email)
    print("Password", password)
    
    user = getUserByEmail(email)

    if user and user["senha"] == hashed:
        payload = {
            "sub": user["email"],
            "role": user["role"],
            "exp": time.time() + TOKEN_EXPIRATION
        }

        access_payload = payload.copy()
        access_payload["type"] = "access"

        access_token = create_jwt(access_payload)
        refresh_token = create_refresh_token(payload)

        handler._send_json({
            "access_token": access_token,
            "refresh_token": refresh_token
        })
    else:
        handler._send_json({"error": "Credenciais inválidas"}, 401)


def post_Refresh(handler):
    content_length = int(handler.headers.get("Content-Length", 0))
    body = handler.rfile.read(content_length).decode('utf-8')

    try:
        data = json.loads(body)
    except:
        handler._send_json({"error": "JSON inválido"}, 400)
        return

    refresh_token = data.get("refresh_token")

    if not refresh_token:
        handler._send_json({"error": "Refresh token não enviado"}, 400)
        return

    payload = verify_jwt(refresh_token)

    if not payload:
        handler._send_json({"error": "Refresh token inválido"}, 401)
        return

    if payload.get("type") != "refresh":
        handler._send_json({"error": "Token inválido para refresh"}, 401)
        return

    new_payload = {
        "sub": payload["sub"],
        "role": payload["role"],
        "type": "access",
        "exp": time.time() + TOKEN_EXPIRATION
    }

    access_token = create_jwt(new_payload)

    handler._send_json({
        "access_token": access_token
    })

def post_Logout(handler):
    content_length = int(handler.headers.get("Content-Length", 0))
    body = handler.rfile.read(content_length).decode('utf-8')

    try:
        data = json.loads(body)
    except:
        handler._send_json({"error": "JSON inválido"}, 400)
        return

    refresh_token = data.get("refresh_token")

    if not refresh_token:
        handler._send_json({"error": "Refresh token não informado"}, 400)
        return

    invalidate_token(refresh_token)

    handler._send_json({"message": "Logout realizado com sucesso"})