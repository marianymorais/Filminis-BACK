DROP DATABASE IF EXISTS filme_mari;
CREATE DATABASE filme_mari;
USE filme_mari;

-- Tabelas básicas
CREATE TABLE pais (
  id_pais INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(255) NOT NULL
);

CREATE TABLE genero (
  id_genero INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(255) NOT NULL
);

CREATE TABLE linguagem (
  id_linguagem INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(255) NOT NULL
);

CREATE TABLE categoria (
  id_categoria INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(255) NOT NULL
);

CREATE TABLE produtora (
  id_produtora INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(255) NOT NULL
);

-- Pessoas
CREATE TABLE ator (
  id_ator INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(255) NOT NULL,
  sobrenome VARCHAR(255) NOT NULL,
  id_genero INT NOT NULL,
  FOREIGN KEY (id_genero) REFERENCES genero(id_genero)
);

CREATE TABLE diretor (
  id_diretor INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(255) NOT NULL,
  sobrenome VARCHAR(255) NOT NULL,
  id_genero INT NOT NULL,
  FOREIGN KEY (id_genero) REFERENCES genero(id_genero)
);

CREATE TABLE filme_pais (
  id_filme_pais INT AUTO_INCREMENT PRIMARY KEY,
  id_filme INT NOT NULL,
  id_pais INT NOT NULL,

  FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
  FOREIGN KEY (id_pais) REFERENCES pais(id_pais)
);

-- Países das pessoas e produtoras
CREATE TABLE ator_pais (
  id_ator_pais INT PRIMARY KEY AUTO_INCREMENT,
  id_ator INT NOT NULL,
  id_pais INT NOT NULL,
  FOREIGN KEY (id_ator) REFERENCES ator(id_ator),
  FOREIGN KEY (id_pais) REFERENCES pais(id_pais)
);

CREATE TABLE diretor_pais  (
  id_diretor_pais INT PRIMARY KEY AUTO_INCREMENT,
  id_pais INT NOT NULL,
  id_diretor INT NOT NULL,
  FOREIGN KEY (id_pais) REFERENCES pais(id_pais),
  FOREIGN KEY (id_diretor) REFERENCES diretor(id_diretor)
);

CREATE TABLE produtora_pais  (
  id_produtora_pais INT PRIMARY KEY AUTO_INCREMENT,
  id_produtora INT NOT NULL,
  id_pais INT NOT NULL,
  FOREIGN KEY (id_produtora) REFERENCES produtora(id_produtora),
  FOREIGN KEY (id_pais) REFERENCES pais(id_pais)
);

-- Filme
CREATE TABLE filme (
  id_filme INT PRIMARY KEY AUTO_INCREMENT,
  titulo VARCHAR(255) NOT NULL,
  id_produtora_principal INT,
  orcamento DECIMAL(15,2),
  duracao TIME,
  ano INT,
  poster VARCHAR(255),
  FOREIGN KEY (id_produtora_principal) REFERENCES produtora(id_produtora)
);

-- Relacionamentos N:N
CREATE TABLE filme_produtora (
  id_filme_produtora INT PRIMARY KEY AUTO_INCREMENT,
  id_filme INT NOT NULL,
  id_produtora INT NOT NULL,
  FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
  FOREIGN KEY (id_produtora) REFERENCES produtora(id_produtora)
);

CREATE TABLE filme_categoria (
  id_filme_categoria INT PRIMARY KEY AUTO_INCREMENT,
  id_filme INT NOT NULL,
  id_categoria INT NOT NULL,
  FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
  FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
);

CREATE TABLE filme_ator (
  id_filme_ator INT PRIMARY KEY AUTO_INCREMENT,
  id_filme INT NOT NULL,
  id_ator INT NOT NULL,
  FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
  FOREIGN KEY (id_ator) REFERENCES ator(id_ator)
);

CREATE TABLE filme_diretor (
  id_filme_diretor INT PRIMARY KEY AUTO_INCREMENT,
  id_filme INT NOT NULL,
  id_diretor INT NOT NULL,
  FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
  FOREIGN KEY (id_diretor) REFERENCES diretor(id_diretor)
);

CREATE TABLE filme_linguagem (
  id_filme_linguagem INT PRIMARY KEY AUTO_INCREMENT,
  id_filme INT NOT NULL,
  id_linguagem INT NOT NULL,
  FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
  FOREIGN KEY (id_linguagem) REFERENCES linguagem(id_linguagem)
);


-- Inserção de dados de exemplo

-- Países
INSERT INTO pais (nome) VALUES
('Estados Unidos'), ('Reino Unido'), ('Japão'),
('Canadá'), ('França'), ('Alemanha'),
('Brasil'), ('Nova Zelândia'), ('Coreia do Sul'), 
('Espanha'), ('México'), ('Chile'),
('Italia'), ('Suécia'), ('Ucrânia'), ('Austrália'),
('Guatemala');

-- Gêneros
INSERT INTO genero (nome) VALUES
('Masculino'), ('Feminino'), ('Não-binario');

-- Linguagens
INSERT INTO linguagem (nome) VALUES
('Inglês'), ('Japonês'), ('Português'), ('Francês'), ('Espanhol'), ('Dinamarquês'), ('Romeno'), ('Romani'), ('Russo'), 
('Latim'), ('Alemão'), ('Italiano'), ('Chines'), ('Coreano'), ('Xhosa'), ('Húngaro'), ('Tagalo'), ('Mandarim');

-- Categorias
INSERT INTO categoria (nome) VALUES
('Ação'), ('Aventura'), ('Animação'), ('Comédia'), ('Crime'), ('Drama'),
('Fantasia'), ('Ficção Científica'), ('Gótico'), ('Musical'), ('Neo-noir'),
('Romance'), ('Super-herói'), ('Suspense'), ('Terror'), ('Thriller');

-- Produtoras
INSERT INTO produtora (nome) VALUES
('Summit Entertainment'),('Studio Ghibli'), ('Regency Enterprises'), ('Millenium Films'),
('6th & Idaho'),('Warner Bros.'), ('Proximity Media'), ('Netflix'),
('Lakeshore Entertainment'), ('20th Century Fox'), ('Marvel Studios'),
('Paramount Pictures'), ('Thunder Road Pictures'),('Legendary Pictures'),('Sony Pictures Animation');

-- Atores
INSERT INTO ator (nome, sobrenome, id_genero) VALUES
('Kristen', 'Stewart', 2), ('Robert', 'Pattinson', 1), ('Taylor', 'Lautner', 1), ('Yōji', 'Matsuda', 1), 
('Yuriko', 'Ishida', 2), ('Yūko', 'Tanaka', 2), ('Bill', 'Skarsgård', 1), ('Lily-Rose', 'Depp', 2), 
('Nicholas', 'Hoult', 1), ('David', 'Harbour', 1), ('Milla', 'Jovovich', 2), ('Zoë', 'Kravitz', 2), 
('Paul', 'Dano', 1), ('David', 'Corenswet', 1), ('Rachel', 'Brosnahan', 2), ('Milly', 'Alcock', 2), 
('Michael', 'B. Jordan', 1), ('Hailee', 'Steinfeld', 2), ('Oscar', 'Isaac', 1), ('Jacob', 'Elordi', 1), 
('Mia', 'Goth', 2), ('Jason', 'Statham', 1), ('Amy', 'Smart', 2), ('Nicole', 'Kidman', 2),
('Ewan', 'McGregor', 1), ('Robert', 'Downey Jr.', 1), ('Chris', 'Evans', 1), ('Mark', 'Ruffalo', 1),
('Chris', 'Hemsworth', 1),('Scarlett', 'Johansson', 2),('Matthew', 'McConaughey', 1),('Anne', 'Hathaway', 2),
('Keanu', 'Reeves', 1),('Michael', 'Nyqvist', 1),('Chieko', 'Baishô', 1),('Takuya', 'Kimura', 1),
('Akihiro', 'Miwa', 1),('Tom', 'Holland', 1),('Zendaya', '', 2),('Benedict', 'Cumberbatch', 1),
('Margot', 'Robbie', 2),('Ryan', 'Gosling', 1),('America', 'Ferrera', 2),('Ryan', 'Reynolds', 1),
('Morena', 'Baccarin', 2),('Timothée', 'Chalamet', 1),('Rebecca', 'Ferguson', 2),('Laurence', 'Fishburne', 1),
('Carrie-Anne', 'Moss', 2),('Arden', 'Cho', 2),('May', 'Hong', 2),('Ji-young', 'Yoo', 2);

-- Diretores
INSERT INTO diretor (nome, sobrenome, id_genero) VALUES
('Catherine', 'Hardwicke', 2),('Hayao', 'Miyazaki', 1),('Robert', 'Eggers', 1),
('Neil', 'Marshall', 1),('Matt', 'Reeves', 1),('James', 'Gunn', 1),
('Ryan', 'Coogler', 1),('Guillermo', 'del Toro', 1),('Mark', 'Neveldine', 1),
('Brian', 'Taylor', 1),('Baz', 'Luhrmann', 1),('Anthony', 'Russo', 1),
('Joe', 'Russo', 1),('Christopher', 'Nolan', 1),('Chad', 'Stahelski', 1),
('Jon', 'Watts', 1),('Greta', 'Gerwig', 2),('Tim', 'Miller', 1),
('Denis', 'Villeneuve', 1), ('Lana', 'Wachowski', 2), ('Lilly ', 'Wachowski', 2), 
('Maggie ', 'Kang', 1), ('Chris  ', 'Appelhans', 1);

-- Filmes
INSERT INTO filme (titulo, id_produtora_principal, orcamento, duracao, ano, poster) VALUES

('Crepúsculo', 1, 37000000, '02:02:00', 2008, 'https://br.web.img2.acsta.net/medias/nmedia/18/87/02/32/19871201.jpg'),
('A Princesa Mononoke', 2, 20000000, '02:13:00', 1997, 'https://i0.wp.com/studioghibli.com.br/wp-content/uploads/2025/03/Poster-Princesa-Mononoke-IMAX-scaled.jpeg?resize=1080%2C1525&ssl=1'),
('Nosferatu', 3, 50000000, '02:12:00', 2024, 'https://m.media-amazon.com/images/I/715BLU5YPZL.jpg'),
('Hellboy', 4, 50000000, '02:01:00', 2019, 'https://img.elo7.com.br/product/zoom/25FA55C/big-poster-filme-hellboy-2019-lo004-tamanho-90x60-cm-hellboy.jpg'),
('The Batman', 5, 185000000, '02:56:00', 2022, 'https://img.elo7.com.br/product/zoom/3FBA809/big-poster-filme-batman-2022-90x60-cm-lo002-poster-batman.jpg'),
('Superman', 6, 225000000, '02:30:00', 2025, 'https://ingresso-a.akamaihd.net/b2b/production/uploads/articles-content/8923869c-f8a6-4258-ba74-4170bf7fb202.jpg'),
('Pecadores', 7, 90000000, '02:17:00', 2025, 'https://ingresso-a.akamaihd.net/prd/img/movie/pecadores/7f6c9699-002e-43a8-adb3-49d2055014fd.webp'),
('Frankenstein', 8, 120000000, '02:30:00', 2025, 'https://s3.amazonaws.com/nightjarprod/content/uploads/sites/130/2025/08/31180656/frankenstein-2025-poster-691x1024.jpg'),
('Adrenalina', 9, 12000000, '01:28:00', 2006, 'https://br.web.img3.acsta.net/medias/nmedia/18/86/97/09/19870658.jpg'),
('Moulin Rouge', 10, 50000000, '02:06:00', 2001, 'https://uauposters.com.br/media/catalog/product/3/4/346820211103-uau-posters-moulin-rouge-filmes.jpg'),
('Vingadores: Ultimato', 11, 356000000, '03:01:00', 2019, 'https://img.elo7.com.br/product/zoom/259A7AA/big-poster-filme-vingadores-ultimato-lo001-tamanho-90x60-cm-poster-marvel.jpg'),
('Interestelar', 12, 165000000, '02:49:00', 2014, 'https://br.web.img3.acsta.net/pictures/14/10/31/20/39/476171.jpg'),
('John Wick', 13, 20000000, '01:41:00', 2014, 'https://img.elo7.com.br/product/zoom/265E435/big-poster-filme-john-wick-lo03-tamanho-90x60-cm-nerd.jpg'),
('O Castelo Animado', 2, 24000000, '01:59:00', 2004, 'https://i.pinimg.com/474x/ec/f5/96/ecf596b4b836dba11873a07b12381088.jpg'),
('Homem-Aranha: Sem Volta Para Casa', 11, 200000000, '02:28:00', 2021, 'https://cinecriticas.com.br/wp-content/uploads/2021/12/Cine1-12.jpg'),
('Barbie', 6, 145000000, '01:54:00', 2023, 'https://uauposters.com.br/media/catalog/product/cache/1/thumbnail/800x930/9df78eab33525d08d6e5fb8d27136e95/4/5/454520230615-uau-posters-barbie-2023-filmes-1.jpg'),
('Deadpool', 10, 58000000, '01:48:00', 2016, 'https://img.elo7.com.br/product/zoom/1E3BBFE/big-poster-do-filme-deadpool-tamanho-90x-0-cm-loot-op-011-geek.jpg'),
('Duna', 14, 165000000, '02:35:00', 2021, 'https://img.elo7.com.br/product/zoom/3E882A2/big-poster-filme-duna-tamanho-90x60-cm-duna.jpg'),
('Matrix', 6, 63000000, '02:16:00', 1999, 'https://img.elo7.com.br/product/zoom/2679A17/big-poster-filme-matrix-lo02-tamanho-90x60-cm-poster-de-filme.jpg'),
('KPop Demon Hunters', 15, 80000000, '01:45:00', 2025, 'https://m.media-amazon.com/images/I/81Mtr7elTnL.jpg');


-- Filme com mais de uma produtora (Vingadores)
INSERT INTO filme_produtora (id_filme, id_produtora) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(11, 11),
(12, 12), (12, 6),
(13, 13),
(14, 2),
(15, 11),
(16, 6),
(17, 10), (17, 11),
(18, 14),
(19, 6),
(20, 15);

-- Filme com mais de um diretor (Vingadores)
INSERT INTO filme_diretor (id_filme, id_diretor) VALUES
(1, 1), 
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9), (9, 10),
(10, 11),
(11, 12), (11, 13),
(12, 14),
(13, 15),
(14, 2),
(15, 16),
(16, 17),
(17, 18),
(18, 19),
(19, 20), (19, 21),
(20, 22), (20, 23);

-- Filme com mais de uma linguagem (Duna)
INSERT INTO filme_linguagem (id_filme, id_linguagem) VALUES
(1, 1),
(2, 2),
(3, 1),
(4, 1),
(5, 1),
(6, 1),
(7, 1),
(8, 1),
(9, 1),
(10, 1),
(11, 1),
(12, 1),
(13, 1),
(14, 2),
(15, 1),
(16, 1),
(17, 1),
(18, 1), (18, 4),  -- Duna em Inglês e Francês
(19, 1),
(20, 5);

-- Categorias
INSERT INTO filme_categoria (id_filme, id_categoria) VALUES
(1, 7), (1, 12), (1, 6),
(2, 7), (2, 2), (2, 3),
(3, 15), (3, 8),
(4, 7), (4, 1), (4, 15),
(5, 1), (5, 6), (5, 11), (5, 13),
(6, 1), (6, 7), (6, 13),
(7, 15), (7, 7), (7, 6),
(8, 15), (8, 6), (8, 8),
(9, 1), (9, 5), (9, 16),
(10, 6), (10, 10), (10, 12),
(11, 1), (11, 2), (11, 7), (11, 13),
(12, 8), (12, 2),
(13, 1), (13, 14),
(14, 7), (14, 3),
(15, 1), (15, 2), (15, 8), (15, 13),
(16, 4), (16, 7),
(17, 1), (17, 4), (17, 13),
(18, 8), (18, 2),
(19, 1), (19, 8),
(20, 3), (20, 7), (20, 10);

-- Atores por filme
INSERT INTO filme_ator (id_filme, id_ator) VALUES
(1, 1), (1, 2), (1, 3),
(2, 4), (2, 5), (2, 6),
(3, 7), (3, 8), (3, 9),
(4, 10), (4, 11),
(5, 2), (5, 12), (5, 13),
(6, 14), (6, 15), (6, 16),
(7, 17), (7, 18),
(8, 19), (8, 20), (8, 21),
(9, 22), (9, 23),
(10, 24), (10, 25),
(11, 26), (11, 27), (11, 28), (11, 29), (11, 30),
(12, 31), (12, 32),
(13, 33), (13, 34),
(14, 35), (14, 36), (14, 37),
(15, 38), (15, 39), (15, 40),
(16, 41), (16, 42), (16, 43),
(17, 44), (17, 45),
(18, 46), (18, 47), (18, 19), (18, 39),
(19, 33), (19, 48), (19, 49), 
(20, 50), (20, 51), (20, 52);

-- Paises por filme / produtora_pais diretor_pais ator_pais
INSERT INTO ator_pais (id_ator, id_pais) VALUES
(1, 1), (2, 2), (3, 1), (4, 3), (5, 3),
(6, 3), (7, 14), (8, 1), (9, 2), (10, 1),
(11, 15), (12, 1), (13, 1), (14, 1), (15, 1),
(16, 16), (17, 1), (18, 1), (19, 17), (20, 16),
(21, 2), (22, 2), (23, 1), (24, 16), (25, 2),
(26, 1), (27, 1), (28, 1), (29, 16), (30, 1),
(31, 1), (32, 1), (33, 4), (34, 14), (35, 3),
(36, 3), (37, 3), (38, 2), (39, 1), (40, 2), 
(41, 16), (42, 4), (43, 1), (44, 1), (45, 7),
(46, 1), (47, 14), (48, 1), (49, 1), (50, 1),
(51, 9), (52, 1);

INSERT INTO diretor_pais (id_diretor, id_pais) VALUES
(1,1), (2,3), (3,1), (4,2), (5,1), (6,1), (7,1), (8,11), (9,1), (10,1),
(11,16), (12,1), (13,1), (14,2), (15,1), (16,1), (17,1), (18,1), (19,4), (20,1),
(21,1), (22,9), (23,1);

INSERT INTO produtora_pais (id_produtora, id_pais) VALUES
(1,1), (2,3), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1),
(11,1), (12,1), (13,1), (14,1), (15,1);

INSERT INTO filme_linguagem (id_filme, id_linguagem) VALUES
(1,1), (2,2), 
(3,1), (3,7), (3,8), (3,9), (3,10), (3,11),
(4,1), (4,5), (4,6), (4,11), 
(5,1), (5,5), (5,10), (5,1), 
(6,1), 
(7,1), (7,13), 
(8,1), (8,6), (8,4),
(9,1), (9,5), (9,1), 
(10,1), (10,4), (10,5), 
(11,1), (11,2), (11,15), (11,11), 
(12,1), 
(13,1), (13,11), (13,16), 
(14,2), 
(15,1), (15,17), 
(16,1), (16,5), 
(17,1), 
(18,1), (18,18), 
(19,1), 
(20,1), (20,14);