import unittest
import requests
from etc.colors import Colors

BASE_URL = "http://localhost:8000"

USER_CRED = {
    "email": "admin@example.com",
    "password": "admin"
}

class TestAuthFlow(unittest.TestCase):
    colors = Colors()

    @classmethod
    def setUpClass(cls):
        print("\nINICIANDO TESTE COMPLETO DE AUTH")

    def test_01_login(self):
        print(self.colors.colorize("\nTESTE 01 — LOGIN", "green"))

        response = requests.post(
            f"{BASE_URL}/send_loginho",
            data=USER_CRED
        )

        print(self.colors.colorize("\nStatus:", "blue"))
        print(response.status_code)

        print(self.colors.colorize("\nCorpo:", "blue"))
        print(response.text)

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.__class__.access_token = data["access_token"]
        self.__class__.refresh_token = data["refresh_token"]

        print(self.colors.colorize("\nAccess token obtido", "magenta"))
        print(self.access_token[:40], "...")

        print(self.colors.colorize("\nRefresh token obtido", "magenta"))
        print(self.refresh_token[:40], "...")

    def test_02_refresh_token(self):
        print(self.colors.colorize("\nTESTE 02 — REFRESH TOKEN", "green"))

        response = requests.post(
            f"{BASE_URL}/refresh",
            json={
                "refresh_token": self.refresh_token
            }
        )

        print(self.colors.colorize("\nStatus:", "blue"))
        print(response.status_code)

        print(self.colors.colorize("\nCorpo:", "blue"))
        print(response.text)

        self.assertEqual(response.status_code, 200)

        new_access = response.json()["access_token"]

        print(self.colors.colorize("\nNovo access token gerado", "magenta"))
        print(new_access[:40], "...")

    def test_03_logout(self):
        print(self.colors.colorize("\nTESTE 03 — LOGOUT", "green"))

        response = requests.post(
            f"{BASE_URL}/logout",
            json={
                "refresh_token": self.refresh_token
            }
        )

        print(self.colors.colorize("\nStatus:", "blue"))
        print(response.status_code)

        print(self.colors.colorize("\nCorpo:", "blue"))
        print(response.text)

        self.assertEqual(response.status_code, 200)

        print(self.colors.colorize("\nLogout realizado com sucesso", "magenta"))

    def test_04_refresh_depois_logout(self):
        print(self.colors.colorize("\nTESTE 04 — REFRESH APÓS LOGOUT (DEVE FALHAR)", "green"))

        response = requests.post(
            f"{BASE_URL}/refresh",
            json={
                "refresh_token": self.refresh_token
            }
        )

        print(self.colors.colorize("\nStatus:", "blue"))
        print(response.status_code)

        print(self.colors.colorize("\nCorpo:", "blue"))
        print(response.text)

        self.assertEqual(response.status_code, 401)

        print(self.colors.colorize("\nRefresh bloqueado após logout", "magenta"))


if __name__ == "__main__":
    unittest.main()