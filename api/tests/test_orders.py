import unittest
from .. import create_app
from ..config.config import config_dict
from ..models.orders import Orders
from ..utils import db
from flask_jwt_extended import create_access_token

class OrderTestCase(unittest.TestCase):
    def setUp(self):
        self.app =  create_app(config=config_dict['test'])

        self.appctx = self.app.app_context

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()


    def tearDown(self):
        db.drop_all()

        self.app = None

        self.appctx.pop()

        self.client = None


    def testGetAllOrders(self):
        token = create_access_token(identity='testuser')

        headers = {
            'Authorization' : f'Bearer {token}'
        }

        response = self.client.get('/orders/orders', headers =headers)

        assert response.status_code == 200

        assert response.json == []


    def test_create_order(self):

        token = create_access_token(identity='testuser')

        headers = {
            'Authorization' : f'Bearer {token}'
        }


        data = {
            'size' : 'LARGE',
            'quantity' : 3,
            'flavour' : 'test flavour'
        }

        response = self.client.post('/order/orders', json=data, headers=headers)

        assert response.status_code == 201

        orders = Orders.query.all()

        assert len(orders) == 1

