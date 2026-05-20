moviequery = """
SELECT
  f.*,
  JSON_ARRAYAGG(
    JSON_OBJECT(
      'id', c.id_categoria,
      'nome', c.nome
    )
  ) AS categorias
FROM filme f
LEFT JOIN filme_categoria fc ON f.id_filme = fc.id_filme
LEFT JOIN categoria c ON fc.id_categoria = c.id_categoria
GROUP BY f.id_filme;
"""