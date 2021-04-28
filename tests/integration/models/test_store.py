from models.store import StoreModel
from models.item import ItemModel
from tests.integration.models.base_test import BaseTest

class StoreTest(BaseTest):
    def test_create_store(self):
        store = StoreModel('teststore')
        self.assertListEqual(store.items.all(), [])
    def test_crud(self):
        with self.app_context():
            store = StoreModel('teststore')
            self.assertIsNone(StoreModel.find_by_name('teststore'))
            store.save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name('teststore'))
            store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name('teststore'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('testitem', 80, 1)
            store.save_to_db()
            item.save_to_db()
            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'testitem')

    def test_store_json(self):
        with self.app_context():
            store = StoreModel('test')
            expected = {'id': 1,
                'name': 'test',
                'items': []
            }
            self.assertDictEqual(store.json(), expected)

    def test_store_json_item(self):
        with self.app_context():
            store = StoreModel('test')
            i = ItemModel('titem', 12, 1)
            store.save_to_db()
            i.save_to_db()

            expected = {'id': 1,
                'name': 'test',
                'items': [{'name': 'titem', 'price': 12.0}]
            }
            self.assertDictEqual(store.json(), expected)