import json, base64, hmac, hashlib, time

""" Vamos criar um JWT do zero
aqui poderiamos usar a biblioteca PyJWT que alguns desses passos 
não existiriam mais.
MAS
um do zero pareceu mais interessante pra mim :D



JWT (JSON Web Token) é um padrão para autenticação e troca segura de informações entre sistemas. Ele é composto por três partes:

Header: Metadados sobre o token (ex.: algoritmo usado).
Payload: Dados que queremos transmitir (ex.: usuário, expiração).
Signature: Assinatura para garantir integridade e autenticidade.

Formato
header.payload.signature




hashlib

Biblioteca do Python que implementa funções de hash (SHA256, MD5, etc.).
Usamos hashlib.sha256 dentro do HMAC.



Base64URL

Serve para transformar dados binários (como assinatura) em texto seguro para URLs.
Evita caracteres problemáticos (+, /) e remove =.



HMAC-SHA256

É o algoritmo usado para assinar o token.
Garante integridade (não foi alterado) e autenticidade (foi gerado com a chave secreta).
HMAC = Hash-based Message Authentication Code.



JSON

Para representar os dados (header e payload) de forma padronizada e legível.



Se mandássemos os bytes da assinatura diretamente, poderiam conter caracteres inválidos para URLs.
Se não assinássemos, qualquer pessoa poderia alterar o payload.
Se não usássemos hash seguro, seria fácil falsificar tokens.

 """


SECRET_KEY = b"supersecreto123" #chave secreta usada para assinar o token, pode ser QUALQUER COISA.
TOKEN_EXPIRATION = 3600  # 1 Hora

# --- FUNÇÕES JWT ---

#transforma bytes em string Base64URL.
#def base64url_encode(data: bytes) -> str:
def base64url_encode(data):
    return base64.urlsafe_b64encode(data).decode().rstrip("=")

#reconstrói os bytes, adicionando padding se necessário.
#def base64url_decode(data: str) -> bytes:
def base64url_decode(data):
    padding = "=" * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding)

""" Quando usamos Base64, os dados são codificados em blocos de 4 caracteres.
Se o tamanho original não for múltiplo de 3 bytes, a codificação adiciona caracteres = no final para completar o bloco.
Exemplo:

Original: abc → Base64: YWJj
Original: ab → Base64: YWI= (tem um = para completar)

No JWT, usamos Base64URL, que remove esses = para deixar a URL mais limpa. """

#def create_jwt(payload: dict) -> str:
def create_jwt(payload):
    header = {"alg": "HS256", "typ": "JWT"} #Cria o header com algoritmo e tipo.
    #Converte header e payload para JSON e depois para Base64URL.
    header_b64 = base64url_encode(json.dumps(header).encode())
    payload_b64 = base64url_encode(json.dumps(payload).encode())
    msg = f"{header_b64}.{payload_b64}".encode()
    #Concatena header.payload e assina com HMAC-SHA256 usando SECRET_KEY.
    signature = hmac.new(SECRET_KEY, msg, hashlib.sha256).digest()
    sig_b64 = base64url_encode(signature)
    #Junta tudo: header.payload.signature.
    return f"{header_b64}.{payload_b64}.{sig_b64}"





#def verify_jwt(token: str) -> dict | None:
def verify_jwt(token):
    try:
        #Divide o token em 3 partes.
        #O JWT tem 3 partes separadas por ponto:
        #header.payload.signature
        #Aqui, pegamos cada parte codificada em Base64URL.
        header_b64, payload_b64, sig_b64 = token.split(".")
        #Recalcula a assinatura e compara com a recebida.
        #A assinatura original foi feita sobre header.payload.
        #Precisamos recriar isso para comparar.
        msg = f"{header_b64}.{payload_b64}".encode()
        #Decodifica o payload.
        #Usamos a mesma chave (SECRET_KEY) e algoritmo (SHA256).
        #digest() retorna os bytes da assinatura.
        expected_sig = hmac.new(SECRET_KEY, msg, hashlib.sha256).digest()
        #Verifica se o token expirou (exp < tempo atual).
        #Convertendo a assinatura calculada para Base64URL.
        #Comparando com a assinatura recebida (sig_b64).
        #Se não bater, token foi adulterado → retorna None.
        if not hmac.compare_digest(base64url_encode(expected_sig), sig_b64):
            return None
        #Decodifica Base64URL → bytes → JSON → dicionário Python.
        payload = json.loads(base64url_decode(payload_b64))
        #Se exp (timestamp de expiração) for menor que o tempo atual, token expirou.
        if payload.get("exp") < time.time():
            return None
        #Retorna payload se tudo estiver ok.
        return payload
    except Exception:
        return None
    



"""
def verify_jwt(token: str) -> dict | None:
    try:
        print("[LOG] Token recebido:", token)

        # 1. Quebrar o token em partes
        header_b64, payload_b64, sig_b64 = token.split(".")
        print("[LOG] Header Base64:", header_b64)
        print("[LOG] Payload Base64:", payload_b64)
        print("[LOG] Assinatura Base64:", sig_b64)

        # 2. Recriar mensagem para assinatura
        msg = f"{header_b64}.{payload_b64}".encode()
        print("[LOG] Mensagem para assinatura:", msg)

        # 3. Calcular assinatura esperada
        expected_sig = hmac.new(SECRET_KEY, msg, hashlib.sha256).digest()
        expected_sig_b64 = base64url_encode(expected_sig)
        print("[LOG] Assinatura esperada (Base64):", expected_sig_b64)

        # 4. Comparar assinaturas
        if not hmac.compare_digest(expected_sig_b64, sig_b64):
            print("[ERRO] Assinatura inválida!")
            return None
        print("[LOG] Assinatura válida!")

        # 5. Decodificar payload
        payload = json.loads(base64url_decode(payload_b64))
        print("[LOG] Payload decodificado:", payload)

        # 6. Verificar expiração
        if payload.get("exp") < time.time():
            print("[ERRO] Token expirado!")
            return None
        print("[LOG] Token válido e não expirado!")

        return payload

    except Exception as e:
        print("[ERRO] Falha na verificação:", e)
        return None
"""


#def auth_token(header_auth: str) -> bool:
def auth_token(header_auth):
    #Verifica se o header começa com Bearer.
    if not header_auth.startswith("Bearer "):
        return False
    
    #Extrai o token e valida.
    token = header_auth.split(" ")[1]
    payload = verify_jwt(token)
    #Retorna True se válido.
    return payload != None

"""
# --- DEMONSTRAÇÃO ---
# Criar token
payload = {"user": "mariany", "exp": time.time() + TOKEN_EXPIRATION}
token = create_jwt(payload)
print("\nToken gerado:", token)

# Validar imediatamente
print("\n[VALIDAÇÃO IMEDIATA]")
verify_jwt(token)

# Esperar para expirar
print("\nAguardando expiração...")
time.sleep(6)

# Validar após expiração
print("\n[VALIDAÇÃO APÓS EXPIRAR]")
verify_jwt(token)




Token gerado: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoibWFyaWFueSIsImV4cCI6MTY5OTk5OTk5OX0.abc123...

[VALIDAÇÃO IMEDIATA]
[LOG] Token recebido: ...
[LOG] Header Base64: ...
[LOG] Payload Base64: ...
[LOG] Assinatura esperada: ...
[LOG] Assinatura válida!
[LOG] Payload decodificado: {'user': 'mariany', 'exp': 1699999999.0}
[LOG] Token válido e não expirado!

Aguardando expiração...

[VALIDAÇÃO APÓS EXPIRAR]
[LOG] Token recebido: ...
[LOG] Assinatura válida!
[LOG] Payload decodificado: {'user': 'mariany', 'exp': 1699999999.0}
[ERRO] Token expirado!"""