import os
import json, hashlib, time
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from infra.database import *
from infra.users_database import *
from infra.actorsDirectors import *
from infra.genresProducers import *
from api.auth import *


USERS = {
    "usuario@mail.com": hashlib.sha256("123456".encode()).hexdigest(),
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

        elif self.path == '/filmes-pendentes':
            header_auth = self.headers.get("Authorization", "")

            if not header_auth.startswith("Bearer "):
                self._send_json({"error": "Token não informado"}, 401)
                return

            token = header_auth.split(" ")[1]
            payload = verify_jwt(token)
            print(token)
            if not payload or payload.get("role") != "admin":
                self._send_json({"error": "Acesso permitido apenas para admin"}, 403)
                return

            filmes = loadFilminhosPendentes() 

            self._send_json(filmes)
        
        elif self.path.startswith('/filme'):
            query_params = parse_qs(urlparse(self.path).query)

            try:
                id = int(query_params.get('id', [''])[0])
            except:
                self._send_json({"error": "ID inválido"}, 400)
                return

            filme = loadFilmini(id)
            print(filme)

            self._send_json(filme)
        
        elif self.path == '/me':
            header_auth = self.headers.get("Authorization", "")

            if not header_auth.startswith("Bearer "):
                self._send_json({"error": "Token não informado"}, 401)
                return

            token = header_auth.split(" ")[1]
            payload = verify_jwt(token)

            if not payload:
                self._send_json({"error": "Token inválido ou expirado"}, 401)
                return

            email = payload.get("sub")

            user = getUserByEmail(email)

            if not user:
                self._send_json({"error": "Usuário não encontrado"}, 404)
                return

            user.pop("senha", None)

            if user.get("data_criacao"):
                user["data_criacao"] = str(user["data_criacao"])

            if user.get("data_nascimento"):
                user["data_nascimento"] = str(user["data_nascimento"])

            self._send_json(user)
        
        elif self.path == '/usuarios':
            header_auth = self.headers.get("Authorization", "")

            if not header_auth.startswith("Bearer "):
                self._send_json({"error": "Token não informado"}, 401)
                return

            token = header_auth.split(" ")[1]
            payload = verify_jwt(token)

            if not payload or payload.get("role") != "admin":
                self._send_json({"error": "Apenas admin pode listar usuários"}, 403)
                return

            usuarios = getUsuarios()

            usuarios = serializeUsuarios(usuarios)

            self._send_json(usuarios)
        

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

                self._send_json({
                    "access_token": access_token,
                    "refresh_token": refresh_token
                })
            else:
                self._send_json({"error": "Credenciais inválidas"}, 401)

        elif self.path == '/register':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')

            try:
                data = json.loads(body)
            except:
                self._send_json({"error": "JSON inválido"}, 400)
                return

            nome = data.get("nome")
            sobrenome = data.get("sobrenome")
            apelido = data.get("apelido")
            email = data.get("email")
            senha = data.get("senha")
            data_nascimento = data.get("data_nascimento")
            imagem = data.get("imagem")

            if not nome or not email or not senha:
                self._send_json(
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
                self._send_json(result, 201)
            else:
                self._send_json({"error": "Erro ao cadastrar usuário"}, 400)

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

            # o Role é que define a 'flag' ela ñ vem do front
            role = payload.get("role")
            flag = True if role == "admin" else False

            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')

            try:
                data = json.loads(body)
            except:
                self._send_json({"error": "JSON inválido"}, 400)
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
                self._send_json(resp, 201)
            else:
                self._send_json(
                    {"message": "Filme enviado para aprovação do administrador"},
                    201
                )
        elif self.path == '/refresh':
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode('utf-8')

            try:
                data = json.loads(body)
            except:
                self._send_json({"error": "JSON inválido"}, 400)
                return

            refresh_token = data.get("refresh_token")

            if not refresh_token:
                self._send_json({"error": "Refresh token não enviado"}, 400)
                return

            payload = verify_jwt(refresh_token)

            if not payload:
                self._send_json({"error": "Refresh token inválido"}, 401)
                return

            if payload.get("type") != "refresh":
                self._send_json({"error": "Token inválido para refresh"}, 401)
                return

            new_payload = {
                "sub": payload["sub"],
                "role": payload["role"],
                "type": "access",
                "exp": time.time() + TOKEN_EXPIRATION
            }

            access_token = create_jwt(new_payload)

            self._send_json({
                "access_token": access_token
            })

        elif self.path == '/logout':
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode('utf-8')

            try:
                data = json.loads(body)
            except:
                self._send_json({"error": "JSON inválido"}, 400)
                return

            refresh_token = data.get("refresh_token")

            if not refresh_token:
                self._send_json({"error": "Refresh token não informado"}, 400)
                return

            invalidate_token(refresh_token)

            self._send_json({"message": "Logout realizado com sucesso"})

    
    def do_PUT(self):
        if self.path.startswith('/aprovafilme'):
            header_auth = self.headers.get("Authorization", "")

            if not header_auth.startswith("Bearer "):
                self._send_json({"error": "Token não informado"}, 401)
                return

            token = header_auth.split(" ")[1]
            payload = verify_jwt(token)

            if not payload or payload.get("role") != "admin":
                self._send_json({"error": "Apenas admin pode aprovar filmes"}, 403)
                return

            params = parse_qs(urlparse(self.path).query)
            filme_id = params.get("id", [None])[0]

            if not filme_id:
                self._send_json({"error": "ID do filme não informado"}, 400)
                return

            sucesso = aprovarFilmini(filme_id)

            if sucesso:
                self._send_json({"message": "Filme aprovado com sucesso"})
            else:
                self._send_json({"error": "Filme não encontrado ou já aprovado"}, 404)
        
        
    def do_PATCH(self):
        if self.path.startswith('/filme'):
            header_auth = self.headers.get("Authorization", "")

            if not header_auth.startswith("Bearer "):
                self._send_json({"error": "Token não informado"}, 401)
                return

            token = header_auth.split(" ")[1]
            payload = verify_jwt(token)

            if not payload or payload.get("role") != "admin":
                self._send_json({"error": "Apenas admin pode editar filmes"}, 403)
                return

            params = parse_qs(urlparse(self.path).query)
            id_filme = params.get("id", [None])[0]

            try:
                id_filme = int(id_filme)
            except:
                self._send_json({"error": "ID inválido"}, 400)
                return

            filme = getFilmeById(id_filme)

            if not filme:
                self._send_json({"error": "Filme não encontrado"}, 404)
                return

            if filme["flag"] == 0:
                self._send_json({"error": "Filme ainda não aprovado"}, 403)
                return

            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')

            try:
                data = json.loads(body)
            except:
                self._send_json({"error": "JSON inválido"}, 400)
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

            self._send_json({"message": "Filme editado com sucesso"})

        elif self.path.startswith('/user/role'):
            header_auth = self.headers.get("Authorization", "")

            if not header_auth.startswith("Bearer "):
                self._send_json({"error": "Token não informado"}, 401)
                return

            token = header_auth.split(" ")[1]
            payload = verify_jwt(token)

            if not payload or payload.get("role") != "admin":
                self._send_json(
                    {"error": "Apenas administradores podem alterar roles"},
                    403
                )
                return

            params = parse_qs(urlparse(self.path).query)
            id_usuario = params.get("id", [None])[0]

            try:
                id_usuario = int(id_usuario)
            except:
                self._send_json({"error": "ID inválido"}, 400)
                return

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")

            try:
                data = json.loads(body)
            except:
                self._send_json({"error": "JSON inválido"}, 400)
                return

            nova_role = data.get("role")

            if nova_role not in ["admin", "user"]:
                self._send_json({"error": "Role inválida"}, 400)
                return

            sucesso = atualizarRoleUser(id_usuario, nova_role)

            if sucesso:
                self._send_json(
                    {"message": f"Role do usuário alterada para {nova_role}"}
                )
            else:
                self._send_json(
                    {"error": "Usuário não encontrado"},
                    404
                )


        elif self.path == '/edit/me':
            header_auth = self.headers.get("Authorization", "")

            if not header_auth.startswith("Bearer "):
                self._send_json({"error": "Token não informado"}, 401)
                return

            token = header_auth.split(" ")[1]
            payload = verify_jwt(token)

            if not payload:
                self._send_json({"error": "Token inválido ou expirado"}, 401)
                return

            email = payload.get("sub")

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode('utf-8')

            try:
                data = json.loads(body)
            except:
                self._send_json({"error": "JSON inválido"}, 400)
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
                self._send_json({"error": "Nenhum campo para atualizar"}, 400)
                return

            patchUsuario(email, campos)

            self._send_json({"message": "Perfil atualizado com sucesso"})


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