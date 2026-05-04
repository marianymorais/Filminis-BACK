import os
import json
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from infra.database import *
from infra.users_database import *
from infra.actorsDirectors import *
from infra.genresProducers import *
from api.jwt import *
from api.handlers.filme import *
from api.handlers.users import *
from api.handlers.auth import *


class MyHandler(SimpleHTTPRequestHandler):

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def list_directory(self, path):
        try:
            with open(os.path.join(path, 'index.html'), 'r') as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read().encode('utf-8'))
                return None
        except FileNotFoundError:
            pass
        return super().list_directory(path)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_GET(self):

        if self.path == "/listagem":
            get_Listagem(self)

        elif self.path == "/atores":
            get_Atores(self)
            
        elif self.path == "/diretores":
            get_Diretores(self)
        
        elif self.path == "/categorias":
            get_Categorias(self)
        
        elif self.path == "/produtoras":
            get_Produtoras(self)
        
        elif self.path == "/linguagens":
            get_Linguagem(self)
        
        elif self.path == "/paises":
            get_Pais(self)

        elif self.path == '/filmes-pendentes':
            get_FilmesPendentes(self)
        
        elif self.path.startswith('/filme'):
            get_Filmes(self)
        
        elif self.path == '/me':
            get_Me(self)
        
        elif self.path == '/usuarios':
            get_Usuarios(self)

    def do_POST(self):
        
        if self.path=='/send_loginho':
            post_Loginho(self)

        elif self.path == '/register':
            post_Register(self)

        elif self.path == '/addCat' :
            post_AddCat(self)

        elif self.path == '/cadastrani':
            post_Cadastrani(self)

        elif self.path == '/refresh':
            post_Refresh(self)

        elif self.path == '/logout':
            post_Logout(self)

    
    def do_PUT(self):
        if self.path.startswith('/aprovafilme'):
            put_AprovaFilme(self)
        
        
    def do_PATCH(self):
        if self.path.startswith('/filme'):
            patch_Filme(self)

        elif self.path.startswith('/user/role'):
            patch_UsersRole(self)

        elif self.path == '/edit/me':
            patch_EditMe(self)

    def do_DELETE(self):
        header_auth = self.headers.get("Authorization", "")
        query_params = parse_qs(urlparse(self.path).query)

        try:
            id_item = int(query_params.get('id', [''])[0])
        except:
            self._send_json({"error": "ID inválido"}, 400)
            return

        payload = verify_jwt(header_auth)
        if not payload:
            self._send_json({"error": "Token inválido ou expirado"}, 401)
            return

        if payload.get("role") != "admin":
            self._send_json({"error": "Apenas administradores podem deletar"}, 403)
            return

        if self.path.startswith('/filme'):
            resultado = deleteFilminho(id_item)

            if resultado is None:
                self._send_json({"error": "Filme não encontrado"}, 404)
            else:
                self._send_json(resultado)
            return

        if self.path.startswith('/atores'):
            resultado = deleteActorsDirector("ator", id_item)
            self._send_json(resultado)
            return

        if self.path.startswith('/diretores'):
            resultado = deleteActorsDirector("diretor", id_item)
            self._send_json(resultado)
            return
        
        if self.path.startswith("/categorias"):
            resultado = deleteGenresProducer("categoria", id_item)
            self._send_json(resultado)
            return

        if self.path.startswith("/produtoras"):
            resultado = deleteGenresProducer("produtora", id_item)
            self._send_json(resultado)
            return

        if self.path.startswith("/linguagens"):
            resultado = deleteGenresProducer("linguagem", id_item)
            self._send_json(resultado)
            return

        if self.path.startswith("/paises"):
            resultado = deleteGenresProducer("pais", id_item)
            self._send_json(resultado)
            return


        self._send_json({"error": "Rota de deleção inválida"}, 404)