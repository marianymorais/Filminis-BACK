from infra.database import *

TABELAS = ["pais", "categoria", "produtora", "linguagem"]


def loadGenresProducer(tabela):
    db = get_connection()
    cursor = db.cursor()

    if tabela not in TABELAS:
        raise ValueError("Tabela inválida!")
    
    query = f"SELECT * FROM {tabela} ORDER BY nome"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    db.close()

    listaGP = [
        {
            "id": item[0],
            "nome": item[1]
        }
        for item in results
    ]
    return listaGP

def insertGenresProducer(tabela, nome):
    if tabela not in TABELAS:
        raise ValueError("Tabela inválida!")

    db = get_connection()
    cursor = db.cursor()


    cursor.execute(
        f"SELECT * FROM {tabela} WHERE nome = %s",
        (nome,)
    )
    if cursor.fetchone():
        cursor.close()
        db.close()
        return {"error": f"{nome} já existe em {tabela}"}


    cursor.execute(
        f"INSERT INTO {tabela} (nome) VALUES (%s)",
        (nome,)
    )

    db.commit()
    cursor.close()
    db.close()

    return loadGenresProducer(tabela)

def deleteGenresProducer(tabela, id_item):
    if tabela not in TABELAS:
        raise ValueError("Tabela inválida!")

    db = get_connection()
    cursor = db.cursor()


    cursor.execute(f"SELECT * FROM {tabela} WHERE id_{tabela} = %s", (id_item,))
    if not cursor.fetchone():
        cursor.close()
        db.close()
        return {"error": f"{tabela} não encontrado"}

    if tabela == "categoria":
        cursor.execute(
            "SELECT * FROM filme_categoria WHERE id_categoria = %s",
            (id_item,)
        )

    elif tabela == "produtora":
        cursor.execute(
            "SELECT * FROM filme_produtora WHERE id_produtora = %s",
            (id_item,)
        )

    elif tabela == "linguagem":
        cursor.execute(
            "SELECT * FROM filme_linguagem WHERE id_linguagem = %s",
            (id_item,)
        )

    elif tabela == "pais":
        cursor.execute(
            "SELECT * FROM filme_pais WHERE id_pais = %s",
            (id_item,)
        )

    if cursor.fetchone():
        cursor.close()
        db.close()
        return {
            "error": f"Não é possível deletar {tabela}. Está vinculado a um ou mais filmes."
        }


    cursor.execute(
        f"DELETE FROM {tabela} WHERE id_{tabela} = %s",
        (id_item,)
    )

    db.commit()
    cursor.close()
    db.close()

    return loadGenresProducer(tabela)

