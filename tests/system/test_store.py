from models.store import StoreModel
from tests.base_test import BaseTest
import json
from models.item import ItemModel

class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                req = client.post('/store/name')

                self.assertEqual(req.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('name'))
                self.assertDictEqual(json.loads(req.data), {'name':'name', 'items':[]})

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/name')
                req = client.post('/store/name')

                self.assertEqual(req.status_code, 400)
                self.assertEqual(json.loads(req.data), {'message': "A store with name 'name' already exists."})

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                req = client.post('/store/name')

                self.assertEqual(req.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('name'))
                req = client.delete('/store/name')
                self.assertDictEqual(json.loads(req.data), {'message': 'Store deleted'})
                self.assertIsNone(StoreModel.find_by_name('name'))
                self.assertEqual(req.status_code, 200)

    def test_get_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/name')
                req = client.get('/store/name')
                self.assertDictEqual(json.loads(req.data), {'name': 'name', 'items':[]})

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():

                req = client.get('/store/name')
                self.assertDictEqual(json.loads(req.data), {'message': 'Store not found'})
                self.assertEqual(req.status_code, 404)
    def test_get_store_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()
                ItemModel('itemtest', 12, 1).save_to_db()
                req = client.get('/store/teststore')

                self.assertDictEqual(json.loads(req.data), {'name': 'teststore',
                                                            'items': [{'name':'itemtest', 'price':12}]})

    def test_get_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()
                StoreModel('testst2').save_to_db()
                ItemModel('itemtest', 12, 1).save_to_db()

                req = client.get('/stores')

                self.assertDictEqual(json.loads(req.data), {'stores': [{'name': 'teststore',
                                                            'items': [{'name': 'itemtest', 'price': 12}]},
                                                             {'name': 'testst2', 'items': [] }]
                                                            })
    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()
                StoreModel('testst2').save_to_db()

                req = client.get('/stores')

                self.assertDictEqual(json.loads(req.data), {'stores': [{'name': 'teststore',
                                                                        'items': []},
                                                                       {'name': 'testst2', 'items': []}]
                                                            })