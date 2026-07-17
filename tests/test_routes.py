"""
Test cases for the Account Service routes
"""
import unittest

from service import create_app
from service.models import Account, db
from tests.factories import AccountFactory

BASE_URL = "/accounts"


######################################################################
#  R o u t e   T e s t   C a s e s
######################################################################
class TestAccountService(unittest.TestCase):
    """Test Cases for the Account Service"""

    @classmethod
    def setUpClass(cls):
        """Runs once before the whole test suite"""
        cls.app = create_app(
            {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
        )

    def setUp(self):
        """Runs before each test"""
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        db.session.query(Account).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """Runs after each test"""
        db.session.remove()
        self.app_context.pop()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_accounts(self, count):
        """Factory method to create accounts in bulk"""
        accounts = []
        for _ in range(count):
            account = AccountFactory()
            response = self.client.post(BASE_URL, json=account.serialize())
            self.assertEqual(
                response.status_code, 201, "Could not create test Account"
            )
            new_account = response.get_json()
            account.id = new_account["id"]
            accounts.append(account)
        return accounts

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """It should get 200_OK from the Home Page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "Account REST API Service")
        self.assertEqual(data["version"], "1.0")

    def test_security_headers(self):
        """It should return security headers from Talisman"""
        response = self.client.get("/", environ_overrides={"wsgi.url_scheme": "https"})
        self.assertEqual(response.status_code, 200)
        headers = {
            "X-Frame-Options": "SAMEORIGIN",
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "default-src 'self'; object-src 'none'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }
        for key, value in headers.items():
            self.assertEqual(response.headers.get(key), value)

    def test_cors_security(self):
        """It should return a CORS header"""
        response = self.client.get("/", headers={"Origin": "http://example.com"})
        self.assertEqual(response.status_code, 200)
        # flask-cors allows all origins: it answers with "*" or echoes the origin
        self.assertIn(
            response.headers.get("Access-Control-Allow-Origin"),
            ["*", "http://example.com"],
        )

    # ----------------------------------------------------------
    # CREATE
    # ----------------------------------------------------------
    def test_create_account(self):
        """It should create a new Account"""
        account = AccountFactory()
        response = self.client.post(BASE_URL, json=account.serialize())
        self.assertEqual(response.status_code, 201)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_account = response.get_json()
        self.assertEqual(new_account["name"], account.name)
        self.assertEqual(new_account["email"], account.email)
        self.assertEqual(new_account["address"], account.address)
        self.assertEqual(new_account["phone_number"], account.phone_number)
        self.assertEqual(new_account["date_joined"], account.date_joined.isoformat())

        # Check that the location header points to the new account
        response = self.client.get(location)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], account.name)

    def test_create_account_with_missing_data(self):
        """It should not create an Account with missing data"""
        response = self.client.post(BASE_URL, json={"name": "not enough data"})
        self.assertEqual(response.status_code, 400)

    def test_create_account_with_no_content_type(self):
        """It should not create an Account with no Content-Type"""
        response = self.client.post(BASE_URL, data="bad data")
        self.assertEqual(response.status_code, 415)

    def test_create_account_with_wrong_content_type(self):
        """It should not create an Account with the wrong Content-Type"""
        response = self.client.post(
            BASE_URL, data="hello", content_type="text/html"
        )
        self.assertEqual(response.status_code, 415)

    # ----------------------------------------------------------
    # LIST
    # ----------------------------------------------------------
    def test_list_accounts(self):
        """It should list all Accounts"""
        self._create_accounts(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_list_accounts_empty(self):
        """It should return an empty list when there are no Accounts"""
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    # ----------------------------------------------------------
    # READ
    # ----------------------------------------------------------
    def test_get_account(self):
        """It should read a single Account"""
        account = self._create_accounts(1)[0]
        response = self.client.get(f"{BASE_URL}/{account.id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], account.name)

    def test_get_account_not_found(self):
        """It should not read an Account that is not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("could not be found", data["message"])

    # ----------------------------------------------------------
    # UPDATE
    # ----------------------------------------------------------
    def test_update_account(self):
        """It should update an existing Account"""
        account = self._create_accounts(1)[0]
        update_payload = account.serialize()
        update_payload["name"] = "Updated Name"
        response = self.client.put(f"{BASE_URL}/{account.id}", json=update_payload)
        self.assertEqual(response.status_code, 200)
        updated_account = response.get_json()
        self.assertEqual(updated_account["name"], "Updated Name")

    def test_update_account_not_found(self):
        """It should not update an Account that is not found"""
        account = AccountFactory()
        response = self.client.put(f"{BASE_URL}/0", json=account.serialize())
        self.assertEqual(response.status_code, 404)

    def test_update_account_with_bad_data(self):
        """It should not update an Account with bad data"""
        account = self._create_accounts(1)[0]
        response = self.client.put(f"{BASE_URL}/{account.id}", json={})
        self.assertEqual(response.status_code, 400)

    # ----------------------------------------------------------
    # DELETE
    # ----------------------------------------------------------
    def test_delete_account(self):
        """It should delete an Account"""
        account = self._create_accounts(1)[0]
        response = self.client.delete(f"{BASE_URL}/{account.id}")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b"")
        # Make sure it is really gone
        response = self.client.get(f"{BASE_URL}/{account.id}")
        self.assertEqual(response.status_code, 404)

    def test_delete_account_not_found(self):
        """It should return 204 when deleting an Account that does not exist"""
        response = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, 204)

    # ----------------------------------------------------------
    # ERROR HANDLERS
    # ----------------------------------------------------------
    def test_method_not_allowed(self):
        """It should not allow an illegal method call"""
        response = self.client.delete(BASE_URL)
        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main()
