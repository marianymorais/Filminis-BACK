import mysql.connector
from infra.query import *

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mmoraiss",
        database="filme_mari"
    )

def split_info(campo, sep=' | ', sub_sep=' — ', keys=('nome', 'genero')):
    if not campo:
        return []
    partes = campo.split(sep)
    resultado = []
    for parte in partes:
        subpartes = parte.split(sub_sep)
        if len(subpartes) == len(keys):
            resultado.append({k: v.strip() for k, v in zip(keys, subpartes)})
        else:
            resultado.append({"valor": parte.strip()})
    return resultado

def loadFilminhos():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM filme")
    results = cursor.fetchall()
    cursor.close()
    db.close()

    filmes = [
        {
            "id": item[0],
            "titulo": item[1],
            "categoria_id": item[2],
            "orcamento": float(item[3]),
            "duracao": str(item[4]),
            "ano": item[5],
            "imagem": item[6]
        }
        for item in results
    ]
    return filmes

# def insertFilminhos(nome, produtora, orcamento, duracao, ano, poster):
#     db = get_connection()
#     cursor = db.cursor()
#     cursor.execute(
#         "INSERT INTO filme_mari.filme (titulo, id_produtora_principal, orcamento, duracao, ano, poster) VALUES (%s, %s, %s, %s, %s, %s)",
#         (nome, produtora, orcamento, duracao, ano, poster)
#     )
#     cursor.execute("SELECT id_filme FROM filme_mari.filme WHERE titulo = %s", (nome,))
#     id_filme = cursor.fetchone()[0]
#     cursor.execute("SELECT * FROM filme_mari.filme WHERE id_filme = %s", (id_filme,))
#     resultado = cursor.fetchall()
#     db.commit()
#     cursor.close()
#     db.close()
#     return resultado

def insertFilminhos(
    nome,
    produtora_principal,
    produtoras,
    categorias,
    atores,
    diretores,
    linguagens,
    paises,          # ⬅️ NOVO
    orcamento,
    duracao,
    ano,
    poster
):
    db = get_connection()
    cursor = db.cursor()

    # 1️⃣ Filme
    cursor.execute(
        """
        INSERT INTO filme
        (titulo, id_produtora_principal, orcamento, duracao, ano, poster)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (nome, produtora_principal, orcamento, duracao, ano, poster)
    )

    id_filme = cursor.lastrowid

    # 2️⃣ Produtoras N:N
    for id_produtora in produtoras:
        cursor.execute(
            "INSERT INTO filme_produtora (id_filme, id_produtora) VALUES (%s, %s)",
            (id_filme, id_produtora)
        )

    # 3️⃣ Categorias
    for id_categoria in categorias:
        cursor.execute(
            "INSERT INTO filme_categoria (id_filme, id_categoria) VALUES (%s, %s)",
            (id_filme, id_categoria)
        )

    # 4️⃣ Atores
    for id_ator in atores:
        cursor.execute(
            "INSERT INTO filme_ator (id_filme, id_ator) VALUES (%s, %s)",
            (id_filme, id_ator)
        )

    # 5️⃣ Diretores
    for id_diretor in diretores:
        cursor.execute(
            "INSERT INTO filme_diretor (id_filme, id_diretor) VALUES (%s, %s)",
            (id_filme, id_diretor)
        )

    # 6️⃣ Linguagens
    for id_linguagem in linguagens:
        cursor.execute(
            "INSERT INTO filme_linguagem (id_filme, id_linguagem) VALUES (%s, %s)",
            (id_filme, id_linguagem)
        )

    # 7️⃣ Países do filme
    for id_pais in paises:
        cursor.execute(
            "INSERT INTO filme_pais (id_filme, id_pais) VALUES (%s, %s)",
            (id_filme, id_pais)
        )

    db.commit()
    cursor.close()
    db.close()

    return {
        "message": "Filme inserido com sucesso",
        "id_filme": id_filme
    }


def loadFilmini(id):
    print(id)
    db = get_connection()
    cursor = db.cursor()
    cursor.execute(queryFilmini, (id,))
    item = cursor.fetchone()

    if item:
            filme = {
                "id": item[0],
                "titulo": item[1],
                "ano": item[2],
                "duracao": str(item[3]),
                "orcamento": float(item[4]),
                "poster": item[5],
                "produtora_principal": item[6],
                "produtoras": split_info(item[7], sep=' | ', sub_sep=' — ', keys=('nome', 'paises')),
                "categorias": [cat.strip() for cat in item[8].split(',')] if item[8] else [],
                "linguagens": [lang.strip() for lang in item[9].split(',')] if item[9] else [],
                "diretores": split_info(item[10], sep=' | ', sub_sep=' — ', keys=('nome', 'genero', 'paises')), #keys=('nome', 'genero', 'paises'))
                "atores": split_info(item[11], sep=' | ', sub_sep=' — ', keys=('nome', 'genero', 'paises')) #keys=('nome', 'genero', 'paises'))
            }
            return filme
    else:
        return None



def deleteFilminho(id_filme):
    db = get_connection()
    cursor = db.cursor()

    # 1. Verifica se o filme existe
    cursor.execute(
        "SELECT id_filme FROM filme WHERE id_filme = %s",
        (id_filme,)
    )

    if not cursor.fetchone():
        cursor.close()
        db.close()
        return None

    # 2. Remove relacionamentos (N:N)
    cursor.execute("DELETE FROM filme_ator WHERE id_filme = %s", (id_filme,))
    cursor.execute("DELETE FROM filme_categoria WHERE id_filme = %s", (id_filme,))
    cursor.execute("DELETE FROM filme_diretor WHERE id_filme = %s", (id_filme,))
    cursor.execute("DELETE FROM filme_linguagem WHERE id_filme = %s", (id_filme,))
    cursor.execute("DELETE FROM filme_produtora WHERE id_filme = %s", (id_filme,))

    # 3. Remove o filme
    cursor.execute(
        "DELETE FROM filme WHERE id_filme = %s",
        (id_filme,)
    )

    db.commit()
    cursor.close()
    db.close()

    return {
        "message": "Filme deletado com sucesso",
        "id_filme": id_filme
    }


#pegar Produtoras
#pegar diretores
#pegar atores
#pegar paises
#pegar linguagens
#pegar generos

#add Produtoras
#add diretores
#add atores
#add paises
#add linguagens
#add generos

#del Produtoras
#del diretores
#del atores
#del paises
#del linguagens
#del generos
