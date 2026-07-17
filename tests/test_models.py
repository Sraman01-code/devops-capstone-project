"""
Test cases for the Account Model
"""
import unittest
from datetime import date

from service import create_app
from service.models import Account, DataValidationError, db
from tests.factories import AccountFactory


######################################################################
#  Account   M o d e l   T e s t   C a s e s
######################################################################
class TestAccountModel(unittest.TestCase):
    """Test Cases for the Account Model"""

    @classmethod
    def setUpClass(cls):
        """Runs once before the whole test suite"""
        cls.app = create_app(
            {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
        )

    def setUp(self):
        """Runs before each test"""
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
    #  T E S T   C A S E S
    ######################################################################

    def test_create_an_account(self):
        """It should create an Account and assert that it exists"""
        fake_account = AccountFactory()
        account = Account(
            name=fake_account.name,
            email=fake_account.email,
            address=fake_account.address,
            phone_number=fake_account.phone_number,
            date_joined=fake_account.date_joined,
        )
        self.assertIsNotNone(account)
        self.assertIsNone(account.id)
        self.assertEqual(account.name, fake_account.name)
        self.assertEqual(account.email, fake_account.email)
        self.assertEqual(account.address, fake_account.address)
        self.assertEqual(account.phone_number, fake_account.phone_number)
        self.assertEqual(account.date_joined, fake_account.date_joined)

    def test_add_an_account(self):
        """It should add an Account to the database"""
        accounts = Account.all()
        self.assertEqual(accounts, [])
        account = AccountFactory()
        account.create()
        self.assertIsNotNone(account.id)
        accounts = Account.all()
        self.assertEqual(len(accounts), 1)

    def test_repr(self):
        """It should have a string representation"""
        account = AccountFactory(name="Foo")
        self.assertIn("Foo", repr(account))

    def test_read_an_account(self):
        """It should read an Account from the database"""
        account = AccountFactory()
        account.create()
        found_account = Account.find(account.id)
        self.assertEqual(found_account.id, account.id)
        self.assertEqual(found_account.name, account.name)
        self.assertEqual(found_account.email, account.email)

    def test_update_an_account(self):
        """It should update an Account in the database"""
        account = AccountFactory(email="before@example.com")
        account.create()
        self.assertIsNotNone(account.id)
        account.email = "after@example.com"
        account.update()
        found_account = Account.find(account.id)
        self.assertEqual(found_account.email, "after@example.com")

    def test_update_with_no_id_raises_error(self):
        """It should not update an Account with no id"""
        account = AccountFactory()
        account.id = None
        self.assertRaises(DataValidationError, account.update)

    def test_delete_an_account(self):
        """It should delete an Account from the database"""
        account = AccountFactory()
        account.create()
        self.assertEqual(len(Account.all()), 1)
        account.delete()
        self.assertEqual(len(Account.all()), 0)

    def test_list_all_accounts(self):
        """It should list all Accounts in the database"""
        for _ in range(5):
            AccountFactory().create()
        self.assertEqual(len(Account.all()), 5)

    def test_find_returns_none_when_not_found(self):
        """It should return None when an Account is not found"""
        self.assertIsNone(Account.find(0))

    def test_serialize_an_account(self):
        """It should serialize an Account into a dictionary"""
        account = AccountFactory()
        serial_account = account.serialize()
        self.assertEqual(serial_account["id"], account.id)
        self.assertEqual(serial_account["name"], account.name)
        self.assertEqual(serial_account["email"], account.email)
        self.assertEqual(serial_account["address"], account.address)
        self.assertEqual(serial_account["phone_number"], account.phone_number)
        self.assertEqual(serial_account["date_joined"], account.date_joined.isoformat())

    def test_deserialize_an_account(self):
        """It should deserialize an Account from a dictionary"""
        data = AccountFactory().serialize()
        account = Account()
        account.deserialize(data)
        self.assertEqual(account.name, data["name"])
        self.assertEqual(account.email, data["email"])
        self.assertEqual(account.address, data["address"])
        self.assertEqual(account.phone_number, data["phone_number"])
        self.assertEqual(account.date_joined, date.fromisoformat(data["date_joined"]))

    def test_deserialize_defaults_date_joined(self):
        """It should default date_joined to today when it is missing"""
        data = AccountFactory().serialize()
        del data["date_joined"]
        account = Account()
        account.deserialize(data)
        self.assertEqual(account.date_joined, date.today())

    def test_deserialize_with_missing_key_raises_error(self):
        """It should not deserialize an Account with missing data"""
        data = {"id": 1, "name": "not enough data"}
        account = Account()
        self.assertRaises(DataValidationError, account.deserialize, data)

    def test_deserialize_with_bad_data_raises_error(self):
        """It should not deserialize bad data"""
        account = Account()
        self.assertRaises(DataValidationError, account.deserialize, "bad data")
        self.assertRaises(DataValidationError, account.deserialize, None)

    def test_deserialize_with_bad_date_raises_error(self):
        """It should not deserialize an Account with a bad date"""
        data = AccountFactory().serialize()
        data["date_joined"] = "not-a-date"
        account = Account()
        self.assertRaises(DataValidationError, account.deserialize, data)


if __name__ == "__main__":
    unittest.main()
