from models.user import UserModel
from models.store import StoreModel
from models.item import ItemModel

from tests.base_test import BaseTest
import json

class ItemTest(BaseTest):
    def setUp(self): #this setup will override the setup of the BaseTest and it will break the tests so:
        super(ItemTest, self).setUp() #this thing calls the setup method of the BaseTest
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_req = client.post('/auth',
                                       data = json.dumps({'username': 'test', 'password': '1234'}),
                                       headers = {'Content-Type':'application/json'})
                auth_token = json.loads(auth_req.data)['access_token']
                self.access_token = {'Authorization': 'JWT '+auth_token}
    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')
                self.assertEqual(resp.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():

                resp = client.get('/item/test', headers =self.access_token)
                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 12, 1).save_to_db()
                resp = client.get('/item/test', headers=self.access_token)
                self.assertEqual(resp.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 12, 1).save_to_db()
                resp = client.delete('/item/test')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.post('/item/test',  data = { 'price': 12, 'store_id': 1})
                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual(json.loads(resp.data), {'name':'test', 'price':12})

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 12, 1).save_to_db()
                resp = client.post('/item/test', data={'price': 12, 'store_id': 1})
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': "An item with name 'test' already exists."}, json.loads(resp.data))

    def test_put_new_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                resp = client.put('/item/test', data={'price': 12, 'store_id': 1})
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test', 'price': 12})

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 12, 1).save_to_db()
                resp = client.put('/item/test', data={'price': 11, 'store_id': 1})
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test', 'price': 11})

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 12, 1).save_to_db()
                ItemModel('test1', 12, 1).save_to_db()
                resp = client.get('/items')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'items': [{'name': 'test', 'price': 12},
                                                                       {'name': 'test1', 'price': 12}] })
    def test_empty_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                resp = client.get('/items')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'items': [] })

    def test_items_list_many_stores(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 12, 1).save_to_db()
                ItemModel('test1', 12, 1).save_to_db()
                StoreModel('test2').save_to_db()
                ItemModel('test2', 2, 2).save_to_db()
                resp = client.get('/items')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'items': [{'name': 'test', 'price': 12},
                                                                       {'name': 'test1', 'price': 12},
                                                                       {'name': 'test2', 'price': 2}] })