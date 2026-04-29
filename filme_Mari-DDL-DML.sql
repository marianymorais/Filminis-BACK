DROP DATABASE IF EXISTS filme_mari;
CREATE DATABASE filme_mari;
USE filme_mari;
DROP TABLE IF EXISTS usuario;
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
  sinopse LONGTEXT,
  ano INT,
  poster VARCHAR(255),
  flag BOOLEAN,
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

CREATE TABLE filme_pais (
  id_filme_pais INT AUTO_INCREMENT PRIMARY KEY,
  id_filme INT NOT NULL,
  id_pais INT NOT NULL,

  FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
  FOREIGN KEY (id_pais) REFERENCES pais(id_pais)
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


-- CRIAÇÃO DAS TABELAS DE USUÁRIOS

CREATE TABLE usuario (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  sobrenome VARCHAR(255),
  apelido VARCHAR(100),
  email VARCHAR(255) NOT NULL UNIQUE,
  senha VARCHAR(255) NOT NULL,
  data_nascimento DATE,
  imagem VARCHAR(500), -- link da imagem
  role ENUM('admin','user') NOT NULL DEFAULT 'user',
  data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
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
INSERT INTO filme (titulo, id_produtora_principal, orcamento, duracao, sinopse, ano, poster, flag) VALUES

('Crepúsculo', 1, 37000000, '02:02:00', "Bella Swan has always been a little bit different. Never one to run with the crowd, Bella never cared about fitting in with the trendy girls at her Phoenix, Arizona high school. When her mother remarries and Bella chooses to live with her father in the rainy little town of Forks, Washington, she doesn't expect much of anything to change. But things do change when she meets the mysterious and dazzlingly beautiful Edward Cullen. For Edward is nothing like any boy she's ever met. He's nothing like anyone she's ever met, period. He's intelligent and witty, and he seems to see straight into her soul. In no time at all, they are swept up in a passionate and decidedly unorthodox romance - unorthodox because Edward really isn't like the other boys. He can run faster than a mountain lion. He can stop a moving car with his bare hands. Oh, and he hasn't aged since 1918. Like all vampires, he's immortal. That's right - vampire. But he doesn't have fangs - that's just in the movies. And he doesn't drink human blood, though Edward and his family are unique among vampires in that lifestyle choice. To Edward, Bella is that thing he has waited 90 years for - a soul mate. But the closer they get, the more Edward must struggle to resist the primal pull of her scent, which could send him into an uncontrollable frenzy. Somehow or other, they will have to manage their unmanageable love. But when unexpected visitors come to town and realize that there is a human among them Edward must fight to save Bella? A modern, visual, and visceral Romeo and Juliet story of the ultimate forbidden love affair - between vampire and mortal." , 2008, 'https://br.web.img2.acsta.net/medias/nmedia/18/87/02/32/19871201.jpg', true),
('A Princesa Mononoke', 2, 20000000, '02:13:00', "While protecting his village from rampaging boar-god/demon, a confident young warrior, Ashitaka, is stricken by a deadly curse. To save his life, he must journey to the forests of the west. Once there, he's embroiled in a fierce campaign that humans were waging on the forest. The ambitious Lady Eboshi and her loyal clan use their guns against the gods of the forest and a brave young woman, Princess Mononoke, who was raised by a wolf-god. Ashitaka sees the good in both sides and tries to stem the flood of blood. This is met by animosity by both sides as they each see him as supporting the enemy." , 1997, 'https://i0.wp.com/studioghibli.com.br/wp-content/uploads/2025/03/Poster-Princesa-Mononoke-IMAX-scaled.jpeg?resize=1080%2C1525&ssl=1', true),
('Nosferatu', 3, 50000000, '02:12:00', "Wisborg, Germany, 1838. Saddled by his superior with the urgent task of sealing a land deal, newlywed estate agent Thomas Hutter reluctantly abandons his worried wife, Ellen, in hopes of securing his position in the firm. However, the mesmerising sight of lustrous gold is a deadly trap; as the ambitious young realtor arrives at the mysterious Count Orlok's isolated castle in the Carpathian Alps, the ghastly embodiment of pure horror begins to haunt Ellen's unspoken nocturnal imaginings. With the light succumbing to darkness, who can ease the suffocating stranglehold of ancient evil? After all, few have gazed into the abyss and lived to tell the tale. Can willing sacrifice rid Wisborg of the Nosferatu?", 2024, 'https://m.media-amazon.com/images/I/715BLU5YPZL.jpg', true),
('Hellboy', 4, 50000000, '02:01:00', "Hellboy is a supernatural being who is the son of a fallen angel. He came to our world in 1944 as a result of a mystical ritual. The Occultists of the Third Reich had long tried to gain an advantage in the war, hoping to attract the ideal soldier to the ranks of the fascist army. Hellboy was exactly the one they needed, but they never managed to make their plans a reality. The demon from hell fell into the hands of Americans and began to serve them, protecting the world from mysterious threats. This time he is sent to England to meet face to face with Merlin's wife. Just a battle with the Blood Queen will lead to the end of the world, which the monster tried to avoid all his life", 2019, 'https://img.elo7.com.br/product/zoom/25FA55C/big-poster-filme-hellboy-2019-lo004-tamanho-90x60-cm-hellboy.jpg', true),
('The Batman', 5, 185000000, '02:56:00', "Two years of nights have turned Bruce Wayne into a nocturnal animal. But as he continues to find his way as Gotham's dark knight, Bruce is forced into a game of cat and mouse with his biggest threat so far, a manic killer known as 'The Riddler' who is filled with rage and determined to expose the corrupt system whilst picking off all of Gotham's key political figures. Working with both established and new allies, Bruce must track down the killer and see him brought to justice, while investigating his father's true legacy and questioning the effect that he has had on Gotham so far as 'The Batman.'", 2022, 'https://img.elo7.com.br/product/zoom/3FBA809/big-poster-filme-batman-2022-90x60-cm-lo002-poster-batman.jpg', true),
('Superman', 6, 225000000, '02:30:00', "Set within a new DC universe. A few years into his heroics, Superman embarks on a personal quest to understand his Kryptonian heritage and mix it with his upbringing as mild mannered Clark Kent. But things get complicated when ruthless industrialist Lex Luthor frames Superman for an international incident and plans to put himself on top by bringing Superman down. Now with aid from Lois Lane, Jimmy Olsen and the Justice Gang, Superman must embrace his lineage and fully become the hero we deserve in order to stop Luthor's plot and save the world.", 2025, 'https://ingresso-a.akamaihd.net/b2b/production/uploads/articles-content/8923869c-f8a6-4258-ba74-4170bf7fb202.jpg', true),
('Pecadores', 7, 90000000, '02:17:00', "1930s. Brothers 'Smoke' and 'Stack' Moore return home to Mississippi after working for the Chicago Mafia. They buy a sawmill and a juke joint and use their experience as gangsters to ensure that their businesses flourish. Things appear to be going well but trouble has just hit town, trouble in supernatural form.", 2025, 'https://ingresso-a.akamaihd.net/prd/img/movie/pecadores/7f6c9699-002e-43a8-adb3-49d2055014fd.webp', true),
('Frankenstein', 8, 120000000, '02:30:00', "Oscar-winning director Guillermo del Toro adapts Mary Shelley's classic tale of Victor Frankenstein, a brilliant but egotistical scientist who brings a creature to life in a monstrous experiment that ultimately leads to the undoing of both the creator and his tragic creation.", 2025, 'https://s3.amazonaws.com/nightjarprod/content/uploads/sites/130/2025/08/31180656/frankenstein-2025-poster-691x1024.jpg', true),
('Adrenalina', 9, 12000000, '01:28:00', "Poisoned by the potent and deadly mix of synthetic drugs called 'The Beijing Cocktail' for getting in the way of the Triads, the tough-as-nails British hitman living in Los Angeles, Chev Chelios, wakes up with a terrible headache. With less than an hour to live, Chev will have to use all the help he can get from his doctor, and use every trick in the book, to consistently keep his heart rate up so that the adrenaline in his bloodstream staves off the effects of the deadly toxin. Now, his heart is pounding faster than any other human being, and as Chelios darts across the city's streets in search of an antidote and the arrogant criminal, Ricky Verona, to exact his revenge, he finds himself compelled to pick fights with no-nonsense drug dealers, murderous assassins, and an army of thugs. But, can Chelios stay alive long enough to protect those he loves, and make it through the day?", 2006, 'https://br.web.img3.acsta.net/medias/nmedia/18/86/97/09/19870658.jpg', true),
('Moulin Rouge', 10, 50000000, '02:06:00', "The year is 1899, and Christian, a young English writer, has come to Paris to follow the Bohemian revolution taking hold of the city's drug and prostitute infested underworld. And nowhere is the thrill of the underworld more alive than at the Moulin Rouge, a night club where the rich and poor men alike come to be entertained by the dancers, but things take a wicked turn for Christian as he starts a deadly love affair with the star courtesan of the club, Satine. But her affections are also coveted by the club's patron: the Duke. A dangerous love triangle ensues as Satine and Christian attempt to fight all odds to stay together but a force that not even love can conquer is taking its toll on Satine...", 2001, 'https://uauposters.com.br/media/catalog/product/3/4/346820211103-uau-posters-moulin-rouge-filmes.jpg', true),
('Vingadores: Ultimato', 11, 356000000, '03:01:00', "After the devastating events of Avengers: Infinity War (2018), the universe is in ruins due to the efforts of the Mad Titan, Thanos. With the help of remaining allies, the Avengers must assemble once more in order to undo Thanos's actions and undo the chaos to the universe, no matter what consequences may be in store, and no matter who they face...", 2019, 'https://img.elo7.com.br/product/zoom/259A7AA/big-poster-filme-vingadores-ultimato-lo001-tamanho-90x60-cm-poster-marvel.jpg', true),
('Interestelar', 12, 165000000, '02:49:00', "In the near future around the American Midwest, Cooper, an ex-science engineer and pilot, is tied to his farming land with his daughter Murph and son Tom. As devastating sandstorms ravage Earth's crops, the people of Earth realize their life here is coming to an end as food begins to run out. Eventually stumbling upon a N.A.S.A. base 6 hours from Cooper's home, he is asked to go on a daring mission with a few other scientists into a wormhole because of Cooper's scientific intellect and ability to pilot aircraft unlike the other crew members. In order to find a new home while Earth decays, Cooper must decide to either stay, or risk never seeing his children again in order to save the human race by finding another habitable planet.", 2014, 'https://br.web.img3.acsta.net/pictures/14/10/31/20/39/476171.jpg', true),
('John Wick', 13, 20000000, '01:41:00', "With the untimely death of his beloved wife still bitter in his mouth, John Wick, the expert former assassin, receives one final gift from her--a precious keepsake to help John find a new meaning in life now that she is gone. But when the arrogant Russian mob prince, Iosef Tarasov, and his men pay Wick a rather unwelcome visit to rob him of his prized 1969 Mustang and his wife's present, the legendary hitman will be forced to unearth his meticulously concealed identity. Blind with revenge, John will immediately unleash a carefully orchestrated maelstrom of destruction against the sophisticated kingpin, Viggo Tarasov, and his family, who are fully aware of his lethal capacity. Now, only blood can quench the boogeyman's thirst for retribution.", 2014, 'https://img.elo7.com.br/product/zoom/265E435/big-poster-filme-john-wick-lo03-tamanho-90x60-cm-nerd.jpg', true),
('O Castelo Animado', 2, 24000000, '01:59:00', "With her country's peace constantly under threat, Sophie, a lively but unloved milliner, catches the attention of an unexpected defender. But as the wide-eyed damsel in distress crosses paths with handsome Howl, a talented young magician with excess emotional baggage, a fit of jealousy turns the hat maker's world upside down forever. Now, stained by the indelible mark of the wicked Witch of the Waste, Sophie must move mountains to break the pitiless spell, including facing her fears and the mysterious sorcerer. However, has anyone ever set foot in Howl's impenetrable home, a walking wonder powered by a fiery heart, and lived to tell the tale?", 2004, 'https://i.pinimg.com/474x/ec/f5/96/ecf596b4b836dba11873a07b12381088.jpg', true),
('Homem-Aranha: Sem Volta Para Casa', 11, 200000000, '02:28:00', "Peter Parker's secret identity is revealed to the entire world. Desperate for help, Peter turns to Doctor Strange to make the world forget that he is Spider-Man. The spell goes horribly wrong and shatters the multiverse, bringing in monstrous villains that could destroy the world.",2021, 'https://cinecriticas.com.br/wp-content/uploads/2021/12/Cine1-12.jpg', true),
('Barbie', 6, 145000000, '01:54:00', "Barbie the Doll lives in bliss in the matriarchal society of Barbieland feeling good about her role in the world in the various iterations of Barbies over the years showing girls that play with her that they can be whatever and whoever they want. On the flip side, Ken, who also lives in Barbieland, is unnoticed except in relation to Barbie, which is however one step above any other doll in Barbieland, such as Allan. One day, Stereotypical Barbie begins to have feelings which she's never experienced which leads to her world seemingly falling apart. Weird Barbie determines that there is something happening in the real world with someone playing with her being unhappy leading to Stereotypical Barbie reluctantly heading to the real world to rectify what is happening with that person, she first needing to find this person. Much to Barbie's chagrin, the original Ken, Beach Ken, tags along with her to the real world in he needing to survive in her presence. Beyond their mission to find this person, Barbie and Ken will find the real world unlike anything they know in Barbieland, especially in it being a male dominated society. While Barbie still has to find out what's going on that made her come to the real world, Ken is finding a newfound control which he wants to bring back to Barbieland. If he is able to do so, the role of Barbie in the real world may be forever changed. On top of everything, executives at Mattel, primarily white men, discover that a 'real life' Barbie and Ken doll have infiltrated the real world, their mission to capture the pair, but especially Barbie, to put them/her back in their/her place, namely in a manufacturer's sealed box.", 2023, 'https://uauposters.com.br/media/catalog/product/cache/1/thumbnail/800x930/9df78eab33525d08d6e5fb8d27136e95/4/5/454520230615-uau-posters-barbie-2023-filmes-1.jpg', true),
('Deadpool', 10, 58000000, '01:48:00', "This is the origin story of former Special Forces operative turned mercenary Wade Wilson, who after being subjected to a rogue experiment that leaves him with accelerated healing powers, adopts the alter ego Deadpool. Armed with his new abilities and a dark, twisted sense of humor, Deadpool hunts down the man who nearly destroyed his life", 2016, 'https://img.elo7.com.br/product/zoom/1E3BBFE/big-poster-do-filme-deadpool-tamanho-90x-0-cm-loot-op-011-geek.jpg', true),
('Duna', 14, 165000000, '02:35:00', "A mythic and emotionally charged hero's journey, 'Dune' tells the story of Paul Atreides, a brilliant and gifted young man born into a great destiny beyond his understanding, who must travel to the most dangerous planet in the universe to ensure the future of his family and his people. As malevolent forces explode into conflict over the planet's exclusive supply of the most precious resource in existence-a commodity capable of unlocking humanity's greatest potential-only those who can conquer their fear will survive.", 2021, 'https://img.elo7.com.br/product/zoom/3E882A2/big-poster-filme-duna-tamanho-90x60-cm-duna.jpg', true),
('Matrix', 6, 63000000, '02:16:00', "Thomas A. Anderson is a man living two lives. By day he is an average computer programmer and by night a hacker known as Neo. Neo has always questioned his reality, but the truth is far beyond his imagination. Neo finds himself targeted by the police when he is contacted by Morpheus, a legendary computer hacker branded a terrorist by the government. As a rebel against the machines, Neo must confront the agents: super-powerful computer programs devoted to stopping Neo and the entire human rebellion.", 1999, 'https://img.elo7.com.br/product/zoom/2679A17/big-poster-filme-matrix-lo02-tamanho-90x60-cm-poster-de-filme.jpg', true),
('KPop Demon Hunters', 15, 80000000, '01:45:00', "A world-renowned K-Pop girl group balances their lives in the spotlight with their secret identities as bad-ass demon hunters, set against a colorful backdrop of fashion, food, style, and the most popular music movement of the current generation.", 2025, 'https://m.media-amazon.com/images/I/81Mtr7elTnL.jpg', true);


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

-- usuários 
INSERT INTO usuario (nome, sobrenome, apelido, email, senha, data_nascimento, imagem, role)
VALUES (
	'mariany',
    'morais',
    'mari',
    'admin@example.com',
    SHA2('admin', 256),
    '1995-03-18',
    'imagem',
    'admin'
);

INSERT INTO usuario (nome, sobrenome, apelido, email, senha, data_nascimento, imagem, role)
VALUES (
	'mariany',
    'morais',
    'mari',
    'usuario@mail.com',
    SHA2('123456', 256),
    "1995-03-18",
    'imagem',
    'user'
)
