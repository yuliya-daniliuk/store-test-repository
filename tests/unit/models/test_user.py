from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest

class UserModelTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('name', '123pass')
        self.assertEqual(user.username, 'name')
        self.assertEqual(user.password, '123pass')