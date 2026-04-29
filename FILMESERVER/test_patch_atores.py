import unittest
import requests

BASE_URL = "http://localhost:8000"

ADMIN_LOGIN = {
    "email": "admin@example.com",
    "password": "admin"
}

class TestPatchAtores(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nLOGIN COMO ADMIN")

        r = requests.post(
            f"{BASE_URL}/send_loginho",
            data=ADMIN_LOGIN
        )

        print("Status login:", r.status_code)
        print("Resposta login:", r.text)

        assert r.status_code == 200, "Falha no login"

        cls.token = r.json()["token"]

        cls.id_filme = 21

        print("Filme usado no teste:", cls.id_filme)

    def test_01_buscar_atores_antes(self):
        print("\nBUSCANDO ATORES ANTES DO PATCH")

        r = requests.get(
            f"{BASE_URL}/filme?id={self.id_filme}"
        )

        print("Status GET:", r.status_code)
        filme = r.json()

        self.assertEqual(r.status_code, 200)

        atores = filme.get("atores", [])

        print("Atores ANTES:", atores)

        # guarda para comparar depois
        self.__class__.atores_antes = atores

        self.assertTrue(len(atores) > 0, "Filme não tem atores")

    def test_02_patch_atores(self):
        print("\nPATCH — ALTERANDO ATORES")

        url = f"{BASE_URL}/filme?id={self.id_filme}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        novos_atores = [1, 2, 3]

        payload = {
            "atores": novos_atores
        }

        print("URL:", url)
        print("Payload:", payload)

        r = requests.patch(url, json=payload, headers=headers)

        print("Status PATCH:", r.status_code)
        print("Resposta PATCH:", r.text)

        self.assertEqual(r.status_code, 200)

    def test_03_buscar_atores_depois(self):
        print("\nBUSCANDO ATORES DEPOIS DO PATCH")

        r = requests.get(
            f"{BASE_URL}/filme?id={self.id_filme}"
        )

        print("Status GET:", r.status_code)
        filme = r.json()

        self.assertEqual(r.status_code, 200)

        atores_depois = filme.get("atores", [])

        print("Atores DEPOIS:", atores_depois)

        self.assertNotEqual(
            self.__class__.atores_antes,
            atores_depois,
            "Atores não foram alterados"
        )

        print("PATCH DE ATORES FUNCIONOU COM SUCESSO")


if __name__ == "__main__":
    unittest.main()
