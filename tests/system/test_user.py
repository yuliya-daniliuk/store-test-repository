from models.user import UserModel
from tests.base_test import BaseTest
import json

class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client: #we get a client to call from this client to api
            with self.app_context(): #we connect to db
                request = client.post('/register', data = {'username': 'test', 'password': '123asd'})
                #data is sent as formdata
                self.assertEqual(request.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created'}, json.loads(request.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '123asd'})
                auth_req = client.post('/auth',
                                       data = json.dumps({'username': 'test', 'password':'123asd'}),
                                       headers = {'Content-Type': 'application/json'})
                                        #converting string into json coz auth wants json not formdata
# auth will return {'access_token': '1231h2g3hj13g1jh23g12jh3g'} we'll check it is indeed sent in response:
                self.assertIn('access_token', json.loads(auth_req.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:  # we get a client to call from this client to api
            with self.app_context():  # we connect to db
                client.post('/register', data={'username': 'test', 'password': '123asd'})
                request = client.post('/register', data={'username': 'test', 'password': '123asd'})
                self.assertEqual(request.status_code, 400)
                self.assertDictEqual({'message': 'A user already exists'}, json.loads(request.data))