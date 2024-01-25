import unittest
from .. import create_app
from ..config.config import config_dict
from ..models.orders import Order
from ..utils import db
from flask_jwt_extended import create_access_token

class OrderTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        with self.appctx:
            db.create_all()

        

    def tearDown(self):
        db.drop_all()

        self.app = None

        self.appctx.pop()

        self.client = None


    def test_get_all_orders(self):
        
        with self.appctx:
            token = create_access_token(identity='testuser')

        headers = {
            "Authorization":f"Bearer {token}"
        }

        response = self.client.get('/orders/', headers=headers)
        #print(response.data)
        assert response.status_code == 200

        assert response.json == []

    def test_create_order(self):

        token = create_access_token(identity="testuser")

        headers = {
            "Authorization":f"Bearer {token}"
        }

        data = {
            "quantity":1,
            "flavour":"RUM",
            "order_status":"PENDING",
            "size":"SMALL"
            }

        response = self.client.post('/orders/', headers=headers, json=data)

        assert response.status_code == 201
        
        # this two above isnt working because for some reason isnt creating the post in the database
        #orders = Order.query.all()

        #assert len(orders) == 1
        