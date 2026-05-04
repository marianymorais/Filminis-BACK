import os
import json, hashlib, time
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from infra.database import *
from infra.users_database import *
from infra.actorsDirectors import *
from infra.genresProducers import *
from api.jwt import *


def get_Listagem(handler):
    filmes = loadFilminhos()
    handler._send_json(filmes)

def get_Atores(handler):
    atores = loadActorsDirector("ator")
    handler._send_json(atores)

def get_Diretores(handler):
    diretores = loadActorsDirector("diretor")
    handler._send_json(diretores)

def get_Categorias(handler):
    categorias = loadGenresProducer("categoria")
    handler._send_json(categorias)

def get_Produtoras(handler):
    produtoras = loadGenresProducer("produtora")
    handler._send_json(produtoras)

def get_Linguagem(handler):
    linguagens = loadGenresProducer("linguagem")
    handler._send_json(linguagens)

def get_Pais(handler):
    paises = loadGenresProducer("pais")
    handler._send_json(paises)

def get_FilmesPendentes(handler):
    header_auth = handler.headers.get("Authorization", "")

    if not header_auth.startswith("Bearer "):
        handler._send_json({"error": "Token não informado"}, 401)
        return

    token = header_auth.split(" ")[1]
    payload = verify_jwt(token)
    print(token)
    if not payload or payload.get("role") != "admin":
        handler._send_json({"error": "Acesso permitido apenas para admin"}, 403)
        return

    filmes = loadFilminhosPendentes() 

    handler._send_json(filmes)

def get_Filmes(handler):
    query_params = parse_qs(urlparse(handler.path).query)

    try:
        id = int(query_params.get('id', [''])[0])
    except:
        handler._send_json({"error": "ID inválido"}, 400)
        return

    filme = loadFilmini(id)
    print(filme)

    handler._send_json(filme)

def post_AddCat(handler):
    header_auth = handler.headers.get("Authorization", "")
    content_length = int(handler.headers['Content-length'])
    body = handler.rfile.read(content_length).decode('utf-8')
    form_data = parse_qs(body)

    propriedade = form_data.get('cat', [""])[0]
    nome = str(form_data.get('nome', [""])[0])

    print("Data form:")
    print("Propriedade:", propriedade)
    print("Nome", nome)
    r = "" 
    tabela = ""

    match propriedade:
        case "Atores Principais":
            tabela = "ator"
            name = nome.split()
            print(name[0], name[1])
            r = insertActorDirector(tabela, name[0], name[1])
        case "Diretores":
            tabela = "diretor"
            name = nome.split()
            r = insertActorDirector(tabela, name[0], name[1])
        case "Linguagem":
            tabela = "linguagem"
            r = insertGenresProducer(tabela, nome)
        case "País de Origem":
            tabela = "pais"
            r = insertGenresProducer(tabela, nome)
        case "Produtora":
            tabela = "produtora"
            r = insertGenresProducer(tabela, nome)
        case "Categorias":
            tabela = "categoria"
            r = insertGenresProducer(tabela, nome)
    
    print(tabela, r)

    if auth_token(header_auth):
        handler._send_json(r)
    else:
        handler._send_json({"error": "Token inválido ou expirado"}, 401)


def post_Cadastrani(handler):
    header_auth = handler.headers.get("Authorization", "")

    if not header_auth.startswith("Bearer "):
        handler._send_json({"error": "Token não informado"}, 401)
        return

    token = header_auth.split(" ")[1]
    payload = verify_jwt(token)

    if not payload:
        handler._send_json({"error": "Token inválido ou expirado"}, 401)
        return

    # o Role é que define a 'flag' ela ñ vem do front
    role = payload.get("role")
    flag = True if role == "admin" else False

    content_length = int(handler.headers['Content-Length'])
    body = handler.rfile.read(content_length).decode('utf-8')

    try:
        data = json.loads(body)
    except:
        handler._send_json({"error": "JSON inválido"}, 400)
        return

    nome = data.get("titulo")
    ano = int(data.get("ano"))
    sinopse = data.get("sinopse")
    duracao = data.get("duracao")
    poster = data.get("imagem")

    orcamento_raw = data.get("orcamento", "0")
    orcamento = int(
        orcamento_raw.replace("R$", "").replace(".", "").replace(",", "").strip()
    )

    categorias = data.get("categoria_id", [])
    diretores = data.get("diretor_id", [])
    atores = data.get("atores_ids", [])
    produtoras = data.get("produtora_id", [])
    linguagens = data.get("linguagem_id", [])
    paises = data.get("pais_origem_id", [])

    produtora_principal = produtoras[0] if produtoras else None

    resp = insertFilminhos(
        nome=nome,
        produtora_principal=produtora_principal,
        produtoras=produtoras,
        categorias=categorias,
        atores=atores,
        diretores=diretores,
        linguagens=linguagens,
        paises=paises,
        orcamento=orcamento,
        duracao=duracao,
        sinopse=sinopse,
        ano=ano,
        poster=poster,
        flag=flag 
    )

    if flag:
        handler._send_json(resp, 201)
    else:
        handler._send_json(
            {"message": "Filme enviado para aprovação do administrador"},
            201
        )

def put_AprovaFilme(handler):
    header_auth = handler.headers.get("Authorization", "")

    if not header_auth.startswith("Bearer "):
        handler._send_json({"error": "Token não informado"}, 401)
        return

    token = header_auth.split(" ")[1]
    payload = verify_jwt(token)

    if not payload or payload.get("role") != "admin":
        handler._send_json({"error": "Apenas admin pode aprovar filmes"}, 403)
        return

    params = parse_qs(urlparse(handler.path).query)
    filme_id = params.get("id", [None])[0]

    if not filme_id:
        handler._send_json({"error": "ID do filme não informado"}, 400)
        return

    sucesso = aprovarFilmini(filme_id)

    if sucesso:
        handler._send_json({"message": "Filme aprovado com sucesso"})
    else:
        handler._send_json({"error": "Filme não encontrado ou já aprovado"}, 404)

def patch_Filme(handler):
    header_auth = handler.headers.get("Authorization", "")

    if not header_auth.startswith("Bearer "):
        handler._send_json({"error": "Token não informado"}, 401)
        return

    token = header_auth.split(" ")[1]
    payload = verify_jwt(token)

    if not payload or payload.get("role") != "admin":
        handler._send_json({"error": "Apenas admin pode editar filmes"}, 403)
        return

    params = parse_qs(urlparse(handler.path).query)
    id_filme = params.get("id", [None])[0]

    try:
        id_filme = int(id_filme)
    except:
        handler._send_json({"error": "ID inválido"}, 400)
        return

    filme = getFilmeById(id_filme)

    if not filme:
        handler._send_json({"error": "Filme não encontrado"}, 404)
        return

    if filme["flag"] == 0:
        handler._send_json({"error": "Filme ainda não aprovado"}, 403)
        return

    content_length = int(handler.headers.get('Content-Length', 0))
    body = handler.rfile.read(content_length).decode('utf-8')

    try:
        data = json.loads(body)
    except:
        handler._send_json({"error": "JSON inválido"}, 400)
        return

    campos_para_atualizar = {}

    if "titulo" in data:
        campos_para_atualizar["titulo"] = data["titulo"]

    if "id_produtora_principal" in data:
        campos_para_atualizar["id_produtora_principal"] = data["id_produtora_principal"]

    if "orcamento" in data:
        campos_para_atualizar["orcamento"] = int(
            data["orcamento"]
            .replace("R$", "")
            .replace(".", "")
            .replace(",", "")
            .strip()
        )

    if "duracao" in data:
        campos_para_atualizar["duracao"] = data["duracao"]

    if "sinopse" in data:
        campos_para_atualizar["sinopse"] = data["sinopse"]

    if "ano" in data:
        campos_para_atualizar["ano"] = int(data["ano"])

    if "imagem" in data:
        campos_para_atualizar["poster"] = data["imagem"]

    if campos_para_atualizar:
        patchCamposFilme(id_filme, campos_para_atualizar)

    if "atores" in data:
        patchRelacionamento(id_filme, "filme_ator", "id_ator", data["atores"])

    if "diretores" in data:
        patchRelacionamento(id_filme, "filme_diretor", "id_diretor", data["diretores"])

    if "categorias" in data:
        patchRelacionamento(id_filme, "filme_categoria", "id_categoria", data["categorias"])

    if "linguagens" in data:
        patchRelacionamento(id_filme, "filme_linguagem", "id_linguagem", data["linguagens"])

    if "paises" in data:
        patchRelacionamento(id_filme, "filme_pais", "id_pais", data["paises"])

    if "produtoras" in data:
        patchRelacionamento(id_filme, "filme_produtora", "id_produtora", data["produtoras"])

    handler._send_json({"message": "Filme editado com sucesso"})