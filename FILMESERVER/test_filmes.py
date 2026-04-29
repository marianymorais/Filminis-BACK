import unittest
import requests

BASE_URL = "http://localhost:8000"

ADMIN_CRED = {
    "email": "admin@example.com",
    "password": "admin"
}

USER_CRED = {
    "email": "usuario@mail.com",
    "password": "123456"
}

class TestFilmesFlow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
  
        r_admin = requests.post(
            f"{BASE_URL}/send_loginho",
            data=ADMIN_CRED
        )

        assert r_admin.status_code == 200, r_admin.text
        cls.token_admin = r_admin.json()["token"]

        r_user = requests.post(
            f"{BASE_URL}/send_loginho",
            data=USER_CRED
        )

        assert r_user.status_code == 200, r_user.text
        cls.token_user = r_user.json()["token"]

    def test_01_usuario_cadastra_filme_pendente(self):
        url = f"{BASE_URL}/cadastrani"

        headers = {
            "Authorization": f"Bearer {self.token_user}",
            "Content-Type": "application/json"
        }

        payload = {
            "titulo": "Filme Teste Automático",
            "ano": 2025,
            "duracao": "01:40",
            "sinopse": "Inserido via teste automatizado",
            "imagem": "teste.jpg",
            "orcamento": "R$ 2.000.000",
            "categoria_id": [1],
            "diretor_id": [1],
            "atores_ids": [1],
            "produtora_id": [1],
            "linguagem_id": [1],
            "pais_origem_id": [1]
        }

        response = requests.post(url, json=payload, headers=headers)
        self.assertEqual(response.status_code, 201)

    def test_02_admin_lista_filmes_pendentes(self):
        url = f"{BASE_URL}/filmes-pendentes"

        headers = {
            "Authorization": f"Bearer {self.token_admin}"
        }

        response = requests.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)
        
        self.__class__.filme_id = response.json()[0]["id"]

    def test_03_admin_aprova_filme(self):
        self.assertTrue(
            hasattr(self.__class__, "filme_id"),
            "filme_id não foi definido — verifique test_02"
        )

        url = f"{BASE_URL}/aprovafilme?id={self.__class__.filme_id}"
        headers = {
            "Authorization": f"Bearer {self.token_admin}"
        }

        response = requests.put(url, headers=headers)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()