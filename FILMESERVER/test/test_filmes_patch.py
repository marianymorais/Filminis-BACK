
import unittest
import requests
from etc.colors import Colors

BASE_URL = "http://localhost:8000"

ADMIN_LOGIN = {
    "email": "admin@example.com",
    "password": "admin"
}
colors = Colors()

class TestPatchFilme(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        print(colors.colorize("\nINICIANDO LOGIN COMO ADMIN...", "green"))

        response = requests.post(
            f"{BASE_URL}/send_loginho",
            data=ADMIN_LOGIN
        )

        print(colors.colorize("Status do login:", "blue"))
        print(response.status_code)
        print(colors.colorize("Resposta do login:", "blue"))
        print(response.text)

        assert response.status_code == 200, "Falha no login do admin"

        cls.token_admin = response.json()["token"]

        print(colors.colorize("Login realizado com sucesso", "green"))
        print(colors.colorize("Token recebido:", "blue"))
        print(cls.token_admin[:30], "...")

        # ID de um filme que já existe no banco e tem flag = true
        cls.id_filme = 21

        print("Filme escolhido para o teste (ID):", cls.id_filme)

    def test_01_patch_edita_titulo_e_ano(self):

        print(colors.colorize("\nTESTE 01 — PATCH: editar título e ano", "green"))

        url = f"{BASE_URL}/filme?id={self.id_filme}"

        headers = {
            "Authorization": f"Bearer {self.token_admin}",
            "Content-Type": "application/json"
        }

        payload = {
            "titulo": "Matrix (Editado via PATCH)",
            "ano": 2000
        }

        print(colors.colorize("URL:", "blue"), url)
        print(colors.colorize("Payload enviado:", "blue"), payload)

        response = requests.patch(url, json=payload, headers=headers)

        print(colors.colorize("Status da resposta:","blue"), response.status_code)
        print(colors.colorize("Corpo da resposta:", "blue"), response.text)

        self.assertEqual(response.status_code, 200)
        print(colors.colorize("PATCH de título e ano realizado com sucesso","green"))

    def test_02_patch_edita_apenas_sinopse(self):
        print(colors.colorize("\nTESTE 02 — PATCH: editar apenas a sinopse","green"))

        url = f"{BASE_URL}/filme?id={self.id_filme}"

        headers = {
            "Authorization": f"Bearer {self.token_admin}",
            "Content-Type": "application/json"
        }

        payload = {
            "sinopse": "Sinopse alterada utilizando PATCH, sem mexer em outros campos."
        }

        print(colors.colorize("URL:","blue"), url)
        print(colors.colorize("Payload enviado:","blue"), payload)

        response = requests.patch(url, json=payload, headers=headers)

        print(colors.colorize("Status da resposta:","blue"), response.status_code)
        print(colors.colorize("Corpo da resposta:","blue"), response.text)

        self.assertEqual(response.status_code, 200)
        print(colors.colorize("PATCH parcial (somente sinopse) realizado com sucesso","green"))


if __name__ == "__main__":
    unittest.main()