import json, base64, hmac, hashlib, time


SECRET_KEY = b"supersecreto123" #chave secreta usada para assinar o token, pode ser QUALQUER COISA.
TOKEN_EXPIRATION = 3600  # 1 Hora
REFRESH_EXPIRATION = 86400  # 24 horas
BLACKLIST = set()


def base64url_encode(data):
    return base64.urlsafe_b64encode(data).decode().rstrip("=")

def base64url_decode(data):
    padding = "=" * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding)


def create_jwt(payload):
    header = {"alg": "HS256", "typ": "JWT"} 
   
    header_b64 = base64url_encode(json.dumps(header).encode())
    payload_b64 = base64url_encode(json.dumps(payload).encode())
    msg = f"{header_b64}.{payload_b64}".encode()
   
    signature = hmac.new(SECRET_KEY, msg, hashlib.sha256).digest()
    sig_b64 = base64url_encode(signature)
  
    return f"{header_b64}.{payload_b64}.{sig_b64}"


def verify_jwt(token):
    try:
        
        if token in BLACKLIST:
            return None

        header_b64, payload_b64, sig_b64 = token.split(".")
        msg = f"{header_b64}.{payload_b64}".encode()
        expected_sig = hmac.new(SECRET_KEY, msg, hashlib.sha256).digest()
        if not hmac.compare_digest(base64url_encode(expected_sig), sig_b64):
            return None

        payload = json.loads(base64url_decode(payload_b64))
      
        if payload.get("exp") < time.time():
            return None
      
        return payload
    except Exception:
        return None


def auth_token(header_auth):
  
    if not header_auth.startswith("Bearer "):
        return False
    
    token = header_auth.split(" ")[1]
    payload = verify_jwt(token)
 
    return payload != None


def create_refresh_token(payload):
    payload_refresh = payload.copy()

    payload_refresh["exp"] = time.time() + REFRESH_EXPIRATION
    payload_refresh["type"] = "refresh"

    return create_jwt(payload_refresh)


def invalidate_token(token):
    BLACKLIST.add(token)
