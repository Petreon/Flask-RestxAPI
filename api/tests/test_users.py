import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from http import HTTPStatus
from ..models.users import User

class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        #creating an app context
        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()
        ## create the database in memory seted in config
        with self.appctx:
            db.create_all()
        

    def tearDown(self):
        ## destroying the application
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None

    def test_user_registration(self):

        data = {
            "username":"testuser",
            "email":"testuser@company.com",
            "password":"testpassword"
        }

        response = self.client.post('/auth/signup', json=data)

        user = User.query.filter_by(email = data['email']).first()

        assert user.username == 'testuser'

        assert response.status == '201 CREATED'

    
    def test_login(self):

        data = {
            "email": "testuser@gmail.com",
            "password":"testpassword"
        }

        response = self.client.post('/auth/login', json=data)

        assert response.status == '200 OK'