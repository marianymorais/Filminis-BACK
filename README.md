Adicione o sql no banco de dados</br>
</br>
troque a senha do banco no arquivo</br>
.\FILMESERVER\infra\database.py</br>
</br>
instale a extensão do sql </br>
</br>
python -m pip install mysql-connector-python
</br>
para rodar o back </br>
entre na pasta FILMESERVER </br>
rode </br>
py server.py





{
  "nome": "Mariany",
  "sobrenome": "Morais",
  "apelido": "Mari",
  "email": "mari@email.com",
  "senha": "123456",
  "data_nascimento": "1995-03-10",
  "imagem": "https://link-da-imagem.com/foto.jpg"
}



[
  {
    "id_usuario": 1,
    "nome": "Admin",
    "sobrenome": "Sistema",
    "apelido": "Root",
    "email": "admin@example.com",
    "data_nascimento": null,
    "imagem": null,
    "role": "admin",
    "data_criacao": "2026-04-27 10:00:00"
  },
  {
    "id_usuario": 2,
    "nome": "Teste",
    "apelido": "Tester",
    "email": "user@email.com",
    "role": "user"
  }
]