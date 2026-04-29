import mysql.connector, json
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
            "sinopse":item[5],
            "ano": item[6],
            "imagem": item[7],
            "flag":item[8]
        }
        for item in results
    ]
    return filmes

def insertFilminhos(
    nome,
    produtora_principal,
    produtoras,
    categorias,
    atores,
    diretores,
    linguagens,
    paises,
    orcamento,
    duracao,
    sinopse,
    ano,
    poster,
    flag
):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO filme
        (titulo, id_produtora_principal, orcamento, duracao, sinopse, ano, poster, flag)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (nome, produtora_principal, orcamento, duracao, sinopse, ano, poster, flag)
    )


    id_filme = cursor.lastrowid

    for id_produtora in produtoras:
        cursor.execute(
            "INSERT INTO filme_produtora (id_filme, id_produtora) VALUES (%s, %s)",
            (id_filme, id_produtora)
        )


    for id_categoria in categorias:
        cursor.execute(
            "INSERT INTO filme_categoria (id_filme, id_categoria) VALUES (%s, %s)",
            (id_filme, id_categoria)
        )


    for id_ator in atores:
        cursor.execute(
            "INSERT INTO filme_ator (id_filme, id_ator) VALUES (%s, %s)",
            (id_filme, id_ator)
        )


    for id_diretor in diretores:
        cursor.execute(
            "INSERT INTO filme_diretor (id_filme, id_diretor) VALUES (%s, %s)",
            (id_filme, id_diretor)
        )


    for id_linguagem in linguagens:
        cursor.execute(
            "INSERT INTO filme_linguagem (id_filme, id_linguagem) VALUES (%s, %s)",
            (id_filme, id_linguagem)
        )


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
                "sinopse":item[4],
                "orcamento": float(item[5]),
                "flag":item[6],
                "poster": item[7],
                "produtora_principal": item[8],
                "produtoras": split_info(item[9], sep=' | ', sub_sep=' — ', keys=('nome', 'paises')),
                "categorias": [cat.strip() for cat in item[10].split(',')] if item[10] else [],
                "linguagens": [lang.strip() for lang in item[11].split(',')] if item[11] else [],
                "diretores": split_info(item[12], sep=' | ', sub_sep=' — ', keys=('nome', 'genero', 'paises')), #keys=('nome', 'genero', 'paises'))
                "atores": split_info(item[13], sep=' | ', sub_sep=' — ', keys=('nome', 'genero', 'paises')) #keys=('nome', 'genero', 'paises'))
            }
            return filme
    else:
        return None



def deleteFilminho(id_filme):
    db = get_connection()
    cursor = db.cursor()


    cursor.execute(
        "SELECT id_filme FROM filme WHERE id_filme = %s",
        (id_filme,)
    )

    if not cursor.fetchone():
        cursor.close()
        db.close()
        return None


    cursor.execute("DELETE FROM filme_ator WHERE id_filme = %s", (id_filme,))
    cursor.execute("DELETE FROM filme_categoria WHERE id_filme = %s", (id_filme,))
    cursor.execute("DELETE FROM filme_diretor WHERE id_filme = %s", (id_filme,))
    cursor.execute("DELETE FROM filme_linguagem WHERE id_filme = %s", (id_filme,))
    cursor.execute("DELETE FROM filme_produtora WHERE id_filme = %s", (id_filme,))


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




def loadFilminhosPendentes():

    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM filme WHERE flag = 0")
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
            "sinopse":item[5],
            "ano": item[6],
            "imagem": item[7],
            "flag": bool(item[8])
        }
        for item in results
    ]
    return filmes


def aprovarFilmini(id):
    
    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE filme
        SET flag = true
        WHERE id_filme = %s AND flag = 0
        """,
        (id,)
    )

    db.commit()

    linhas_afetadas = cursor.rowcount

    cursor.close()
    db.close()

    return linhas_afetadas > 0


def patchCamposFilme(id_filme, campos):
    if not campos:
        return

    sets = []
    valores = []

    for campo, valor in campos.items():
        sets.append(f"{campo} = %s")
        valores.append(valor)

    sql = f"""
        UPDATE filme
        SET {', '.join(sets)}
        WHERE id_filme = %s
    """

    valores.append(id_filme)

    db = get_connection()
    cursor = db.cursor()

    cursor.execute(sql, tuple(valores))
    db.commit()

    cursor.close()
    db.close()

def patchRelacionamento(id_filme, tabela, campo_relacionado, novos_ids):
    db = get_connection()
    cursor = db.cursor()

    cursor.execute(
        f"DELETE FROM {tabela} WHERE id_filme = %s",
        (id_filme,)
    )

    for item_id in novos_ids:
        cursor.execute(
            f"""
            INSERT INTO {tabela} (id_filme, {campo_relacionado})
            VALUES (%s, %s)
            """,
            (id_filme, item_id)
        )

    db.commit()
    cursor.close()
    db.close()


def getFilmeById(id_filme):
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM filme WHERE id_filme = %s",
        (id_filme,)
    )

    filme = cursor.fetchone()

    cursor.close()
    db.close()

    return filme