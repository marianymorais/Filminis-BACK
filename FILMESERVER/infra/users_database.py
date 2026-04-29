
import mysql.connector, json, hashlib
from infra.query import *

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mmoraiss",
        database="filme_mari"
    )

def insertUser(
    nome,
    sobrenome,
    apelido,
    email,
    senha,
    data_nascimento=None,
    imagem=None,
    role="user"
):
    db = get_connection()
    cursor = db.cursor()

    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    try:
        cursor.execute(
            """
            INSERT INTO usuario
            (nome, sobrenome, apelido, email, senha, data_nascimento, imagem, role)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                nome,
                sobrenome,
                apelido,
                email,
                senha_hash,
                data_nascimento,
                imagem,
                role
            )
        )

        db.commit()

    except Exception as e:
        print("Erro ao inserir usuário:", e)
        cursor.close()
        db.close()
        return None

    user_id = cursor.lastrowid

    cursor.close()
    db.close()

    return {
        "message": "Usuário cadastrado com sucesso",
        "user": {
                "id": user_id,
                "nome": nome,
                "email": email
            }}

def getUserByEmail(email):
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM usuario WHERE email = %s",
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()
    db.close()

    return user


def atualizarRoleUser(id_usuario, nova_role):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE usuario
        SET role = %s
        WHERE id_usuario = %s
        """,
        (nova_role, id_usuario)
    )

    db.commit()
    sucesso = cursor.rowcount > 0

    cursor.close()
    db.close()

    return sucesso



def patchUsuario(email, campos):
    if not campos:
        return

    sets = []
    valores = []

    for campo, valor in campos.items():
        sets.append(f"{campo} = %s")
        valores.append(valor)

    sql = f"""
        UPDATE usuario
        SET {', '.join(sets)}
        WHERE email = %s
    """

    valores.append(email)

    db = get_connection()
    cursor = db.cursor()

    cursor.execute(sql, tuple(valores))
    db.commit()

    cursor.close()
    db.close()


def serializeUsuarios(lista):
    import datetime

    for user in lista:
        user.pop("senha", None)

        for key in user:
            if isinstance(user[key], (datetime.date, datetime.datetime)):
                user[key] = str(user[key])

    return lista


def getUsuarios():
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuario")

    usuarios = cursor.fetchall()

    cursor.close()
    db.close()

    return usuarios