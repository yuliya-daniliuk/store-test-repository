from models.user import UserModel
from tests.integration.models.base_test import BaseTest

class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('name', '123asd')
            self.assertIsNone(UserModel.find_by_username('name'))
            user.save_to_db()
            self.assertIsNotNone(UserModel.find_by_username('name'))
            self.assertIsNotNone(UserModel.find_by_id(1))


