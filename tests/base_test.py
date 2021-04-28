from unittest import TestCase
from app import app
from db import db

# base test is for integration and sys tests as it lets us use db
class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        #db exists
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['DEBUG'] = False
        app.config['PROPAGATE_EXCEPTIONS'] = True
        with app.app_context():  # as if the app is running
            db.init_app(app)
    def setUp(self):
        #we get a test client
        with app.app_context():
            db.create_all()
        self.app = app.test_client
        self.app_context= app.app_context


    def tearDown(self):
        #db is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()

