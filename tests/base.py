"""TEST - BASE
Definition of BaseTest class, used on all the test classes
"""

# # Native # #
from multiprocessing import Process

# # Installed # #
import httpx
from wait4it import wait_for, get_free_port

# # Project # #
from users_api import run
from users_api.database import users
from users_api.settings import api_settings

__all__ = ("BaseTest",)


class BaseTest:
    api_process: Process
    api_url: str

    @classmethod
    def setup_class(cls):
        # Startup the API on a process before all tests
        # NOTE process can make mocking more difficult
        api_port = api_settings.port = get_free_port()
        cls.api_url = f"http://localhost:{api_port}"
        cls.api_process = Process(target=run, daemon=True)
        cls.api_process.start()
        wait_for(port=api_port)

    @classmethod
    def teardown_class(cls):
        cls.api_process.terminate()

    @classmethod
    def teardown_method(cls):
        # Delete all documents from collection after each test
        users.delete_many({})

    # # API Methods # #

    def get_user(self, user_id: str, statuscode: int = 200):
        r = httpx.get(f"{self.api_url}/users/{user_id}")
        assert r.status_code == statuscode, r.text
        return r

    def list_users(self, statuscode: int = 200):
        r = httpx.get(f"{self.api_url}/users")
        assert r.status_code == statuscode, r.text
        return r

    def create_user(self, create: dict, statuscode: int = 201):
        r = httpx.post(f"{self.api_url}/users", json=create)
        assert r.status_code == statuscode, r.text
        return r

    def update_user(self, user_id: str, update: dict, statuscode: int = 204):
        r = httpx.patch(f"{self.api_url}/users/{user_id}", json=update)
        assert r.status_code == statuscode, r.text
        return r

    def delete_user(self, user_id: str, statuscode: int = 204):
        r = httpx.delete(f"{self.api_url}/users/{user_id}")
        assert r.status_code == statuscode, r.text
        return r
