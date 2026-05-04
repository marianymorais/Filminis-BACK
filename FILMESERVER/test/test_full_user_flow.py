import unittest
import requests
import time
from etc.colors import Colors

BASE_URL = "http://localhost:8000"

colors = Colors()

class TestFullUserFlow(unittest.TestCase):
    

    @classmethod
    def setUpClass(cls):
        print(colors.colorize("\nTESTE COMPLETO DO SISTEMA (USER FLOW)","green"))

        cls.email = f"user_{int(time.time())}@mail.com"
        cls.senha = "123456"

        print(colors.colorize("Usuário:","blue"), cls.email)

    def test_01_register(self):
        print(colors.colorize("\nTESTE 01 — REGISTER", "green"))

        payload = {
            "nome": "Teste",
            "sobrenome": "Automático",
            "apelido": "Tester",
            "email": self.email,
            "senha": self.senha,
            "data_nascimento": "2000-01-01",
            "imagem": "https://imagem.com/teste.jpg"
        }

        r = requests.post(f"{BASE_URL}/register", json=payload)

        print(colors.colorize("\nStatus:", "blue"))
        print(r.status_code)

        print(colors.colorize("\nCorpo:", "blue"))
        print(r.text)

        self.assertEqual(r.status_code, 201)

        print(colors.colorize("Usuário criado", "magenta"))

    def test_02_login(self):
        print(colors.colorize("\nTESTE 02 — LOGIN", "green"))

        r = requests.post(
            f"{BASE_URL}/send_loginho",
            data={
                "email": self.email,
                "password": self.senha
            }
        )

        print(colors.colorize("\nStatus:", "blue"))
        print(r.status_code)

        print(colors.colorize("\nCorpo:", "blue"))
        print(r.text)

        self.assertEqual(r.status_code, 200)

        data = r.json()

        self.__class__.access_token = data["access_token"]
        self.__class__.refresh_token = data["refresh_token"]

        print(colors.colorize("Login OK", "magenta"))

    def test_03_get_me(self):
        print(colors.colorize("\nTESTE 03 — GET /me", "green"))

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        r = requests.get(f"{BASE_URL}/me", headers=headers)

        print(colors.colorize("\nStatus:", "blue"))
        print(r.status_code)

        print(colors.colorize("\nCorpo:", "blue"))
        print(r.text)

        self.assertEqual(r.status_code, 200)

        print(colors.colorize("Perfil carregado", "magenta"))

    def test_04_patch_me(self):
        print(colors.colorize("\nTESTE 04 — PATCH /edit/me'", "green"))

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "apelido": "Atualizado",
            "nome": "Nome Editado"
        }

        r = requests.patch(f"{BASE_URL}/edit/me", json=payload, headers=headers)

        print(colors.colorize("\nStatus:", "blue"))
        print(r.status_code)

        print(colors.colorize("\nCorpo:", "blue"))
        print(r.text)

        self.assertEqual(r.status_code, 200)

        print(colors.colorize("Perfil atualizado", "magenta"))

    def test_05_get_me_atualizado(self):
        print(colors.colorize("\nTESTE 05 — GET /me atualizado", "green"))

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        r = requests.get(f"{BASE_URL}/me", headers=headers)

        print(colors.colorize("\nStatus:", "blue"))
        print(r.status_code)

        print(colors.colorize("\nCorpo:", "blue"))
        print(r.text)

        self.assertEqual(r.status_code, 200)

        self.assertEqual(r.json()["apelido"], "Atualizado")

        print(colors.colorize("Atualização confirmada", "magenta"))

    def test_06_refresh(self):
        print(colors.colorize("\nTESTE 06 — REFRESH TOKEN", "green"))

        r = requests.post(
            f"{BASE_URL}/refresh",
            json={
                "refresh_token": self.refresh_token
            }
        )

        print(colors.colorize("\nStatus:", "blue"))
        print(r.status_code)

        print(colors.colorize("\nCorpo:", "blue"))
        print(r.text)

        self.assertEqual(r.status_code, 200)

        print(colors.colorize("Refresh OK", "magenta"))

    def test_07_logout(self):
        print(colors.colorize("\nTESTE 07 — LOGOUT", "green"))

        r = requests.post(
            f"{BASE_URL}/logout",
            json={
                "refresh_token": self.refresh_token
            }
        )

        print(colors.colorize("\nStatus:", "blue"))
        print(r.status_code)

        print(colors.colorize("\nCorpo:", "blue"))
        print(r.text)

        self.assertEqual(r.status_code, 200)

        print(colors.colorize("Logout realizado", "magenta"))

    def test_08_refresh_depois_logout(self):
        print(colors.colorize("\nTESTE 08 — REFRESH após logout (falha esperada)", "green"))

        r = requests.post(
            f"{BASE_URL}/refresh",
            json={
                "refresh_token": self.refresh_token
            }
        )

        print(colors.colorize("\nStatus:", "blue"))
        print(r.status_code)

        print(colors.colorize("\nCorpo:", "blue"))
        print(r.text)

        self.assertEqual(r.status_code, 401)

        print(colors.colorize("Refresh bloqueado após logout", "magenta"))


if __name__ == "__main__":
    unittest.main()