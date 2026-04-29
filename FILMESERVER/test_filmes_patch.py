import unittest
import requests

BASE_URL = "http://localhost:8000"

ADMIN_LOGIN = {
    "email": "admin@example.com",
    "password": "admin"
}

class TestPatchFilme(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nINICIANDO LOGIN COMO ADMIN...")

        response = requests.post(
            f"{BASE_URL}/send_loginho",
            data=ADMIN_LOGIN
        )

        print("Status do login:", response.status_code)
        print("Resposta do login:", response.text)

        assert response.status_code == 200, "Falha no login do admin"

        cls.token_admin = response.json()["token"]

        print("Login realizado com sucesso")
        print("Token recebido:", cls.token_admin[:30], "...")

        # ID de um filme que já existe no banco e tem flag = true
        cls.id_filme = 21  

        print("Filme escolhido para o teste (ID):", cls.id_filme)

    def test_01_patch_edita_titulo_e_ano(self):
        print("\nTESTE 01 — PATCH: editar título e ano")

        url = f"{BASE_URL}/filme?id={self.id_filme}"

        headers = {
            "Authorization": f"Bearer {self.token_admin}",
            "Content-Type": "application/json"
        }

        payload = {
            "titulo": "Matrix (Editado via PATCH)",
            "ano": 2000
        }

        print("URL:", url)
        print("Payload enviado:", payload)

        response = requests.patch(url, json=payload, headers=headers)

        print("Status da resposta:", response.status_code)
        print("Corpo da resposta:", response.text)

        self.assertEqual(response.status_code, 200)
        print("PATCH de título e ano realizado com sucesso")

    def test_02_patch_edita_apenas_sinopse(self):
        print("\nTESTE 02 — PATCH: editar apenas a sinopse")

        url = f"{BASE_URL}/filme?id={self.id_filme}"

        headers = {
            "Authorization": f"Bearer {self.token_admin}",
            "Content-Type": "application/json"
        }

        payload = {
            "sinopse": "Sinopse alterada utilizando PATCH, sem mexer em outros campos."
        }

        print("URL:", url)
        print("Payload enviado:", payload)

        response = requests.patch(url, json=payload, headers=headers)

        print("Status da resposta:", response.status_code)
        print("Corpo da resposta:", response.text)

        self.assertEqual(response.status_code, 200)
        print("PATCH parcial (somente sinopse) realizado com sucesso")


if __name__ == "__main__":
    unittest.main()