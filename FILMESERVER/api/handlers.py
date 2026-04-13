import os
import json, hashlib, time
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from infra.database import *
from infra.actorsDirectors import *
from infra.genresProducers import *
from api.auth import TOKEN_EXPIRATION, create_jwt, auth_token, verify_jwt

# Simula banco de dados, armazenando senha criptografada
USERS = {
    "marcelo@mail.com": hashlib.sha256("123456".encode()).hexdigest(),
    "admin@example.com": hashlib.sha256("admin".encode()).hexdigest()
}

ADMINS = {"admin@example.com"}

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
            filmes = loadFilminhos()
            self._send_json(filmes)

        elif self.path == "/atores":

            atores = loadActorsDirector("ator")
            self._send_json(atores)
        
        elif self.path == "/diretores":
            diretores = loadActorsDirector("diretor")
            self._send_json(diretores)
        
        elif self.path == "/categorias":
            categorias = loadGenresProducer("categoria")
            self._send_json(categorias)
        
        elif self.path == "/produtoras":
            produtoras = loadGenresProducer("produtora")
            self._send_json(produtoras)
        
        elif self.path == "/linguagens":
            linguagens = loadGenresProducer("linguagem")
            self._send_json(linguagens)
        
        elif self.path == "/paises":
            paises = loadGenresProducer("pais")
            self._send_json(paises)

        elif self.path.startswith('/filme'):
            # header_auth = self.headers.get("Authorization", "")
            query_params = parse_qs(urlparse(self.path).query)
            # print(query_params)
            
            try:
                id = int(query_params.get('id', [''])[0])
            except:
                self._send_json({"error": "ID inválido"}, 400)
                return

            # id = int(query_params.get('id', [''])[0])
            filme = loadFilmini(id)
            print(filme)

            # if auth_token(header_auth):
            self._send_json(filme)
            # else:
            #     self._send_json({"error": "Token inválido ou expirado"}, 401)

    def do_POST(self):
        
        if self.path=='/send_loginho':

            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            email = form_data.get("email", [""])[0]
            password = form_data.get("password", [""])[0]
            hashed = hashlib.sha256(password.encode()).hexdigest()

            print("Data form:")
            print("Email:", email)
            print("Password", password)
            
            if USERS.get(email) == hashed:
                is_admin = email in ADMINS  #ADMINS seria uma lista ou set com emails de administradores
                payload = {
                    "sub": email,
                    "role": "admin" if is_admin else "user",
                    "exp": time.time() + TOKEN_EXPIRATION
                }
                token = create_jwt(payload)
                self._send_json({"token": token})
            else:
                self._send_json({"error": "Credenciais inválidas"}, 401)


        elif self.path == '/addCat' :

            header_auth = self.headers.get("Authorization", "")
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
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
                self._send_json(r)
            else:
                self._send_json({"error": "Token inválido ou expirado"}, 401)

        elif self.path == '/cadastrani':
            header_auth = self.headers.get("Authorization", "")

            if not header_auth.startswith("Bearer "):
                self._send_json({"error": "Token não informado"}, 401)
                return

            token = header_auth.split(" ")[1]
            payload = verify_jwt(token)

            if not payload:
                self._send_json({"error": "Token inválido ou expirado"}, 401)
                return

            if payload.get("role") != "admin":
                self._send_json({"error": "Apenas admin pode cadastrar filmes"}, 403)
                return

            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')

            try:
                data = json.loads(body)
            except:
                self._send_json({"error": "JSON inválido"}, 400)
                return

            nome = data.get("titulo")
            ano = int(data.get("ano"))
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
            ano=ano,
            poster=poster
        )


            self._send_json(resp)

    def do_DELETE(self):
        header_auth = self.headers.get("Authorization", "")
        query_params = parse_qs(urlparse(self.path).query)

        # --- valida ID ---
        try:
            id_item = int(query_params.get('id', [''])[0])
        except:
            self._send_json({"error": "ID inválido"}, 400)
            return

        # --- valida token ---
        payload = verify_jwt(header_auth)
        if not payload:
            self._send_json({"error": "Token inválido ou expirado"}, 401)
            return

        # --- valida admin ---
        if payload.get("role") != "admin":
            self._send_json({"error": "Apenas administradores podem deletar"}, 403)
            return

        # --- DELETE FILME ---
        if self.path.startswith('/filme'):
            resultado = deleteFilminho(id_item)

            if resultado is None:
                self._send_json({"error": "Filme não encontrado"}, 404)
            else:
                self._send_json(resultado)
            return

        # --- DELETE ATOR ---
        if self.path.startswith('/atores'):
            resultado = deleteActorsDirector("ator", id_item)
            self._send_json(resultado)
            return

        # --- DELETE DIRETOR ---
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


        # --- rota inválida ---
        self._send_json({"error": "Rota de deleção inválida"}, 404)