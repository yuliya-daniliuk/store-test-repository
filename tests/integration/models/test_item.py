from models.item import ItemModel
from tests.integration.models.base_test import BaseTest
from models.store import StoreModel

class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            i = ItemModel('m1', 19.99, 1)
            self.assertIsNone(ItemModel.find_by_name('m1'))
            i.save_to_db()
            self.assertIsNotNone(ItemModel.find_by_name('m1'))
            i.delete_from_db()
            self.assertIsNone(ItemModel.find_by_name('m1'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test_item', 12, 1)
            store.save_to_db()
            item.save_to_db()
            self.assertEqual(item.store.name, 'test_store')

