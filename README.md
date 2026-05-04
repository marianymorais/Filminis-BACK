
# Filminis API

Sistema de gerenciamento de filmes com autenticação, controle de usuários e permissões (admin/user).

---

## Sobre o Projeto

O **Filminis API** é um backend desenvolvido em Python que permite:

- Cadastro e gerenciamento de filmes
- Controle de usuários e autenticação via JWT
- Aprovação de filmes por administradores
- Edição de dados com PATCH
- Sistema de login com refresh token e logout


---

## Tecnologias utilizadas

- Python 
- MySQL 
- HTTP Server (SimpleHTTPRequestHandler)
- JWT (implementação própria)
- unittest (testes automatizados)

---

## Estrutura do Projeto


FILMESERVER/
├── handlers/
│   ├── auth.py
│   ├── usuarios.py
│   ├── filmes.py
│
├── infra/
│   ├── database.py
│
├── api/
│   ├── auth.py
│
├── tests/
│   ├── test_full_user_flow.py
│   ├── test_role.py
│   ├── test_patch_atores.py
│
├── server.py
└── README.md


---

## Como rodar o projeto

### 1 Clonar o repositório

```bash
git clone https://seu-repositorio.git
cd FILMESERVER
```

### 2 Instalar dependências
```bash
pip install requests mysql-connector-python
```

### 3 Configurar banco de dados
```bash
Criar banco MySQL
Rodar o script SQL do projeto (filme_mari)
```

### 4 Rodar o servidor
```bash
python server.py
```

---

## O sistema usa JWT com:

Access Token (curta duração)
Refresh Token (renovação)
Logout com blacklist

---

## Autenticação

| Método | Rota            | Descrição                     | Proteção |
|--------|-----------------|------------------------------|----------|
| POST   | /send_loginho   | Realiza login                | Público  |
| POST   | /register       | Cadastra novo usuário        | Público  |
| POST   | /refresh        | Gera novo access token       | Público  |
| POST   | /logout         | Invalida refresh token       | Público  |


## Usuários

| Método | Rota                     | Descrição                         | Proteção     |
|--------|--------------------------|----------------------------------|--------------|
| GET    | /me                      | Retorna perfil do usuário logado | Autenticado  |
| PATCH  | /me                      | Atualiza dados do perfil         | Autenticado  |
| GET    | /usuarios                | Lista todos os usuários          | Admin        |
| PATCH  | /usuario/role?id=...     | Altera role de usuário           | Admin        |


## Filmes

| Método | Rota                         | Descrição                        | Proteção     |
|--------|------------------------------|---------------------------------|--------------|
| GET    | /listagem                    | Lista todos os filmes           | Público      |
| GET    | /filme?id=...                | Retorna detalhes de um filme    | Público      |
| POST   | /cadastrani                 | Cadastra novo filme             | Autenticado  |
| PATCH  | /filme?id=...                | Edita filme (parcial)           | Admin        |
| GET    | /filmes-pendentes            | Lista filmes não aprovados      | Admin        |
| PUT    | /aprovafilme?id=...          | Aprova filme                    | Admin        |


## Dados auxiliares

| Método | Rota         | Descrição              | Proteção |
|--------|--------------|-----------------------|----------|
| GET    | /atores      | Lista atores          | Público  |
| GET    | /diretores   | Lista diretores       | Público  |
| GET    | /categorias  | Lista categorias      | Público  |
| GET    | /produtoras  | Lista produtoras      | Público  |
| GET    | /linguagens  | Lista linguagens      | Público  |
| GET    | /paises      | Lista países          | Público  |