import unittest
import requests
import time
from etc.colors import Colors

BASE_URL = "http://localhost:8000"

class TestRegister(unittest.TestCase):
    colors = Colors()
    @classmethod
    def setUpClass(cls):
        print("\nINICIANDO TESTE DE REGISTER")

        cls.email = f"teste_{int(time.time())}@email.com"
        cls.senha = "123456"

        print("Email gerado:", cls.email)


    def test_01_register_usuario(self):
        print(self.colors.colorize("\nTESTE 01 — Criar usuário", "green"))

        url = f"{BASE_URL}/register"

        payload = {
            "email": self.email,
            "senha": self.senha
        }

        response = requests.post(url, json=payload)

        print(self.colors.colorize("\nStatus:", "green"))
        print(response.status_code)
        print(self.colors.colorize("\nCorpo:", "blue"))
        print(response.text)

        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            response.json()["message"],
            "Usuário cadastrado com sucesso"
        )

        print("Usuário criado com sucesso")

    def test_02_login_usuario_criado(self):
        print(self.colors.colorize("\nTESTE 02 — Login com usuário criado", "green"))
        url = f"{BASE_URL}/send_loginho"

        payload = {
            "email": self.email,
            "password": self.senha
        }

        response = requests.post(url, data=payload)

        
        print(self.colors.colorize("\nStatus:", "green"))
        print(response.status_code)
        
        print(self.colors.colorize("\nCorpo:", "blue"))
        print(response.text)

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

        print(self.colors.colorize("Login funcionando com usuário criado", "magenta"))


if __name__ == "__main__":
    unittest.main()