
from models.item import ItemModel
from tests.unit.unit_base_test import UnitBaseTest

class testItemModel(UnitBaseTest):
    def test_init(self):
        i = ItemModel('model1', 0.95, 1)
        self.assertEqual(i.price, 0.95)
        self.assertEqual(i.store_id, 1)
        self.assertIsNone(i.store) #because sqlite doesnt create the store object, just creates item
        # (other dbs will fail this test, they will need u to create store object before creating items with its foreign key)

    def test_json(self):
        i = ItemModel('model1', 0.95, 1)
        self.assertEqual(i.json(), {'name': 'model1', 'price': 0.95})