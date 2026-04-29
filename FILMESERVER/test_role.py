
import unittest
import requests
import time
from etc.colors import Colors

BASE_URL = "http://localhost:8000"

ADMIN_CRED = {
    "email": "admin@example.com",
    "password": "admin"
}

colors = Colors()

class TestRoleUsuario(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print(colors.colorize("\nINICIANDO TESTE DE ROLE","green"))

        print(colors.colorize("Login ADMIN...","green"))
        r_admin = requests.post(
            f"{BASE_URL}/send_loginho",
            data=ADMIN_CRED
        )

        print(colors.colorize("Status ADMIN:","blue"), r_admin.status_code)
        print(colors.colorize("Resposta ADMIN:","blue"), r_admin.text)

        assert r_admin.status_code == 200

        cls.token_admin = r_admin.json()["access_token"]

        print(colors.colorize("Token ADMIN obtido","green"))

        print(colors.colorize("Criando usuário comum...","green"))

        cls.email_user = f"user_{int(time.time())}@mail.com"
        cls.senha_user = "123456"
        cls.nome_user = "Mariazinha"

        payload = {
            "email": cls.email_user,
            "senha": cls.senha_user,
            "nome": cls.nome_user
        }

        r_register = requests.post(
            f"{BASE_URL}/register",
            json=payload
        )

        print(colors.colorize("Status REGISTER:","blue"), r_register.status_code)
        print(colors.colorize("Resposta REGISTER:","blue"), r_register.text)

        assert r_register.status_code == 201

        cls.id_usuario = r_register.json()["user"]["id"]

        print(colors.colorize("Usuário criado com ID:","magenta"), cls.id_usuario)

        print(colors.colorize("\nLogin USER...","green"))

        r_user = requests.post(
            f"{BASE_URL}/send_loginho",
            data={
                "email": cls.email_user,
                "password": cls.senha_user
            }
        )

        print(colors.colorize("Status USER:","blue"), r_user.status_code)
        print(colors.colorize("Resposta USER:","blue"), r_user.text)

        assert r_user.status_code == 200

        cls.token_user = r_user.json()["access_token"]

        print(colors.colorize("Token USER obtido","magenta"))


    def test_01_user_nao_pode_alterar_role(self):
        print(colors.colorize("\nTESTE 01 — USER tentando alterar role (deve falhar)","green"))

        url = f"{BASE_URL}/user/role?id={self.id_usuario}"

        headers = {
            "Authorization": f"Bearer {self.token_user}",
            "Content-Type": "application/json"
        }

        payload = {
            "role": "admin"
        }

        print(colors.colorize("URL:","blue"), url)
        print(colors.colorize("Payload:","blue"), payload)

        r = requests.patch(url, json=payload, headers=headers)

        print(colors.colorize("Status:","blue"), r.status_code)
        print(colors.colorize("Resposta:","blue"), r.text)

        self.assertEqual(r.status_code, 403)

        print(colors.colorize("Bloqueio correto: USER não pode alterar role","magenta"))


    def test_02_admin_promove_user(self):
        print(colors.colorize("\nTESTE 02 — ADMIN promovendo USER para ADMIN","green"))

        url = f"{BASE_URL}/user/role?id={self.id_usuario}"

        headers = {
            "Authorization": f"Bearer {self.token_admin}",
            "Content-Type": "application/json"
        }

        payload = {
            "role": "admin"
        }

        print(colors.colorize("URL:","blue"), url)
        print(colors.colorize("Payload:","blue"), payload)

        r = requests.patch(url, json=payload, headers=headers)

        print(colors.colorize("Status:","blue"), r.status_code)
        print(colors.colorize("Resposta:","blue"), r.text)

        self.assertEqual(r.status_code, 200)

        print(colors.colorize("Usuário promovido para ADMIN com sucesso","magenta"))

    
    def test_03_admin_lista_usuarios(self):
            print(colors.colorize("\nTESTE03 — LISTAR USUÁRIOS", "green"))

            headers = {
                "Authorization": f"Bearer {self.token_admin}"
            }

            r = requests.get(f"{BASE_URL}/usuarios", headers=headers)

            print(colors.colorize("\nStatus:", "blue"))
            print(r.status_code)

            print(colors.colorize("\nCorpo:", "blue"))
            print(r.text)

            self.assertEqual(r.status_code, 200)
            self.assertTrue(len(r.json()) > 0)

            print(colors.colorize("\n Lista de usuários funcionando", "magenta"))


if __name__ == "__main__":
    unittest.main()