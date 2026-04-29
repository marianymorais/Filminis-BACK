queryFilmini = """
SELECT
  f.id_filme,
  f.titulo,
  f.ano,
  f.duracao,
  f.sinopse,
  f.orcamento,
  f.flag,
  f.poster,
  pp.nome AS produtora_principal,
  (
    SELECT GROUP_CONCAT(prod_info SEPARATOR ' | ')
    FROM (
      SELECT CONCAT(
        p.nome,
        IFNULL(
          CONCAT(' — Países: ',
                 (SELECT GROUP_CONCAT(DISTINCT pa.nome ORDER BY pa.nome SEPARATOR '/')
                  FROM produtora_pais pp2
                  JOIN pais pa ON pa.id_pais = pp2.id_pais
                  WHERE pp2.id_produtora = p.id_produtora)
          ), ''
        )
      ) AS prod_info
      FROM filme_produtora fp
      JOIN produtora p ON p.id_produtora = fp.id_produtora
      WHERE fp.id_filme = f.id_filme
      ORDER BY p.nome
    ) x
  ) AS produtoras,
  (
    SELECT GROUP_CONCAT(DISTINCT c.nome ORDER BY c.nome SEPARATOR ', ')
    FROM filme_categoria fc
    JOIN categoria c ON c.id_categoria = fc.id_categoria
    WHERE fc.id_filme = f.id_filme
  ) AS categorias,
  (
    SELECT GROUP_CONCAT(DISTINCT l.nome ORDER BY l.nome SEPARATOR ', ')
    FROM filme_linguagem fl
    JOIN linguagem l ON l.id_linguagem = fl.id_linguagem
    WHERE fl.id_filme = f.id_filme
  ) AS linguagens,
  (
    SELECT GROUP_CONCAT(dir_info SEPARATOR ' | ')
    FROM (
      SELECT CONCAT(
        d.nome, ' ', d.sobrenome,
        ' — ', g.nome,
        IFNULL(
          CONCAT(' — Países: ',
                 (SELECT GROUP_CONCAT(DISTINCT pa.nome ORDER BY pa.nome SEPARATOR '/')
                  FROM diretor_pais dp2
                  JOIN pais pa ON pa.id_pais = dp2.id_pais
                  WHERE dp2.id_diretor = d.id_diretor)
        ), '')
      ) AS dir_info
      FROM filme_diretor fd
      JOIN diretor d  ON d.id_diretor = fd.id_diretor
      JOIN genero  g  ON g.id_genero  = d.id_genero
      WHERE fd.id_filme = f.id_filme
      ORDER BY d.sobrenome, d.nome
    ) y
  ) AS diretores,
  (
    SELECT GROUP_CONCAT(ator_info SEPARATOR ' | ')
    FROM (
      SELECT CONCAT(
        a.nome, ' ', a.sobrenome,
        ' — ', g.nome,
        IFNULL(
          CONCAT(' — Países: ',
                 (SELECT GROUP_CONCAT(DISTINCT pa.nome ORDER BY pa.nome SEPARATOR '/')
                  FROM ator_pais ap2
                  JOIN pais pa ON pa.id_pais = ap2.id_pais
                  WHERE ap2.id_ator = a.id_ator)
        ), '')
      ) AS ator_info
      FROM filme_ator fa
      JOIN ator a   ON a.id_ator   = fa.id_ator
      JOIN genero g ON g.id_genero = a.id_genero
      WHERE fa.id_filme = f.id_filme
      ORDER BY a.sobrenome, a.nome
    ) z
  ) AS atores
FROM filme f
LEFT JOIN produtora pp ON pp.id_produtora = f.id_produtora_principal
WHERE f.id_filme = %s;
"""



