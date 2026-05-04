
import unittest
import requests
from etc.colors import Colors

BASE_URL = "http://localhost:8000"

ADMIN_CRED = {
    "email": "admin@example.com",
    "password": "admin"
}

USER_CRED = {
    "email": "usuario@mail.com",
    "password": "123456"
}

colors = Colors()

class TestFilmesFlow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        print(colors.colorize("\nLOGIN INICIAL","green"))

        print(colors.colorize("Fazendo login como ADMIN...","blue"))
        r_admin = requests.post(
            f"{BASE_URL}/send_loginho",
            data=ADMIN_CRED
        )

        print(colors.colorize("Status ADMIN:","blue"), r_admin.status_code)
        print(colors.colorize("Resposta ADMIN:","blue"), r_admin.text)

        assert r_admin.status_code == 200, r_admin.text
        cls.token_admin = r_admin.json()["token"]

        print("Token ADMIN obtido")

        print(colors.colorize("\nFazendo login como USER...","green"))
        r_user = requests.post(
            f"{BASE_URL}/send_loginho",
            data=USER_CRED
        )

        print(colors.colorize("Status USER:","blue"), r_user.status_code)
        print(colors.colorize("Resposta USER:","blue"), r_user.text)

        assert r_user.status_code == 200, r_user.text
        cls.token_user = r_user.json()["token"]

        print("Token USER obtido")

    def test_01_usuario_cadastra_filme_pendente(self):
        print(colors.colorize("\nTESTE 01: USUÁRIO CADASTRA FILME","green"))

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

        print(colors.colorize("URL:","blue"), url)
        print(colors.colorize("Payload:","blue"), payload)

        response = requests.post(url, json=payload, headers=headers)

        print(colors.colorize("Status:","blue"), response.status_code)
        print(colors.colorize("Resposta:","blue"), response.text)

        self.assertEqual(response.status_code, 201)

        print("Filme enviado para aprovação (flag = false)")

    def test_02_admin_lista_filmes_pendentes(self):
        print(colors.colorize("\nTESTE 02: ADMIN LISTA PENDENTES","green"))

        url = f"{BASE_URL}/filmes-pendentes"

        headers = {
            "Authorization": f"Bearer {self.token_admin}"
        }

        print(colors.colorize("URL:","blue"), url)

        response = requests.get(url, headers=headers)

        print(colors.colorize("Status:","blue"), response.status_code)
        print(colors.colorize("Resposta:","blue"), response.text)

        self.assertEqual(response.status_code, 200)

        filmes = response.json()
        print(colors.colorize("Filmes pendentes:","blue"), filmes)

        self.assertTrue(len(filmes) > 0)

        self.__class__.filme_id = filmes[0]["id"]

        print(colors.colorize("Filme selecionado para aprovação:","blue"), self.__class__.filme_id)

    def test_03_admin_aprova_filme(self):
        print(colors.colorize("\nTESTE 03: ADMIN APROVA FILME","green"))

        self.assertTrue(
            hasattr(self.__class__, "filme_id"),
            "filme_id não foi definido — verifique test_02"
        )

        url = f"{BASE_URL}/aprovafilme?id={self.__class__.filme_id}"

        headers = {
            "Authorization": f"Bearer {self.token_admin}"
        }

        print(colors.colorize("URL:","blue"), url)

        response = requests.put(url, headers=headers)

        print(colors.colorize("Status:","blue"), response.status_code)
        print(colors.colorize("Resposta:","blue"), response.text)

        self.assertEqual(response.status_code, 200)

        print(colors.colorize("Filme aprovado com sucesso (flag = true)","magenta"))


if __name__ == "__main__":
    unittest.main()
