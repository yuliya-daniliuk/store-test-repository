from models.user import UserModel
from models.store import StoreModel
from models.item import ItemModel

from tests.base_test import BaseTest
import json

class ItemTest(BaseTest):

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')
                self.assertEqual(resp.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_req = client.post('/auth',
                                       data=json.dumps({'username': 'test', 'password': '1234'}),
                                       headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_req.data)['access_token']
                header = {'Authorization': 'JWT ' + auth_token}

                resp = client.get('/item/test', headers =header)
                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 12, 1).save_to_db()
                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)