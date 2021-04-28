from tests.unit.unit_base_test import UnitBaseTest
from models.store import StoreModel

class StoreModelTest(UnitBaseTest):
    def test_create_store(self):
        store= StoreModel('first store')
        self.assertEqual(store.name, 'first store', 'the name of store doent equal the name in constructor')