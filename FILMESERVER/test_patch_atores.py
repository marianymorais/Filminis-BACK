
import unittest
import requests
from etc.colors import Colors

BASE_URL = "http://localhost:8000"

ADMIN_LOGIN = {
    "email": "admin@example.com",
    "password": "admin"
}

colors = Colors()

class TestPatchAtores(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print(colors.colorize("\nLOGIN COMO ADMIN","green"))

        r = requests.post(
            f"{BASE_URL}/send_loginho",
            data=ADMIN_LOGIN
        )

        print(colors.colorize("Status login:","blue"), r.status_code)
        print(colors.colorize("Resposta login:","blue"), r.text)

        assert r.status_code == 200, "Falha no login"

        cls.token = r.json()["token"]

        cls.id_filme = 21

        print(colors.colorize("Filme usado no teste:","blue"), cls.id_filme)

    def test_01_buscar_atores_antes(self):
        print(colors.colorize("\nBUSCANDO ATORES ANTES DO PATCH","green"))

        r = requests.get(
            f"{BASE_URL}/filme?id={self.id_filme}"
        )

        print(colors.colorize("Status GET:","blue"), r.status_code)
        filme = r.json()

        self.assertEqual(r.status_code, 200)

        atores = filme.get("atores", [])

        print(colors.colorize("Atores ANTES:","blue"), atores)

        # guarda para comparar depois
        self.__class__.atores_antes = atores

        self.assertTrue(len(atores) > 0, "Filme não tem atores")

    def test_02_patch_atores(self):
        print(colors.colorize("\nPATCH — ALTERANDO ATORES","green"))

        url = f"{BASE_URL}/filme?id={self.id_filme}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        novos_atores = [1, 2, 3]

        payload = {
            "atores": novos_atores
        }

        print(colors.colorize("URL:","blue"), url)
        print(colors.colorize("Payload:","blue"), payload)

        r = requests.patch(url, json=payload, headers=headers)

        print(colors.colorize("Status PATCH:","blue"), r.status_code)
        print(colors.colorize("Resposta PATCH:","blue"), r.text)

        self.assertEqual(r.status_code, 200)

    def test_03_buscar_atores_depois(self):
        print(colors.colorize("\nBUSCANDO ATORES DEPOIS DO PATCH","green"))

        r = requests.get(
            f"{BASE_URL}/filme?id={self.id_filme}"
        )

        print(colors.colorize("Status GET:","blue"), r.status_code)
        filme = r.json()

        self.assertEqual(r.status_code, 200)

        atores_depois = filme.get("atores", [])

        print(colors.colorize("Atores DEPOIS:","blue"), atores_depois)

        self.assertNotEqual(
            self.__class__.atores_antes,
            atores_depois,
            "Atores não foram alterados"
        )

        print(colors.colorize("PATCH DE ATORES FUNCIONOU COM SUCESSO","green"))


if __name__ == "__main__":
    unittest.main()
