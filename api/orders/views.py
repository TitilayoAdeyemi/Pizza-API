from flask_restx import Namespace, Resource, fields
from ..models.orders import Orders
from ..models.users import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import db



order_namespace = Namespace('order', description='Namespace for orders')

order_model = order_namespace.model(
    'Order', {
    'id': fields.Integer(description='Order id'),
    'size' : fields.String(description='Order size', required =True, enum=['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE']),
    'quantity' : fields.Integer(description='Quantity of orders'),
    'flavour': fields.String(description = True, required=True)
    }
)

order_status_model = order_namespace.model(
    'Order status', {
    'order_status' : fields.String(description='Order status', required=True, enum= ['PENDING', 'IN_TRANSIT', 'DELIVERED'])
    }
)

@order_namespace.route('/orders/')
class CreateAndGetOrder(Resource):
    
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(description = 'Retrieve all orders')
    @jwt_required()
    def get(self):
        """Get all orders"""
        orders=Orders.query.all()

        return orders, HTTPStatus.OK
    
    @order_namespace.expect(order_model)
    @order_namespace.doc(description='Place an order')
    @jwt_required()
    @order_namespace.marshal_with(order_model)
    def post(self):
        """Place an order"""

        username=get_jwt_identity()


        current_user=User.query.filter_by(username=username).first()

        data=order_namespace.payload


        new_order=Orders(
            size=data['size'],
            quantity=data['quantity'],
            flavour=data['flavour']
        )

        new_order.customer=current_user

        new_order.save()

        return new_order, HTTPStatus.CREATED



@order_namespace.route('/orders/<int:order_id>')
class GetUpdateDeleteOrder(Resource): #Gets a particular order, updates it and deletes it using its id
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
            description = 'Retrieves an order by its ID',
            params = {
                'order_id' : 'An ID for a given order'
                }
                    )
    @jwt_required()
    def get(self, order_id):
        """Retrieves an order by id"""
        

        order = Orders.get_by_id(order_id)

        return order, HTTPStatus.OK

    @order_namespace.expect(order_model)
    @order_namespace.doc(
        description = 'Update an order given an order id',
        params = {
        'order_id' : 'An ID for a given order'
        }
        )
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def put(self, order_id):
        """Updates an order using is id"""
        updated_order = Orders.get_by_id(order_id)

        data = order_namespace.payload

        updated_order.quantity = data['quantity']
        updated_order.flavour = data['flavour']
        updated_order.size = data['size']

        db.session.commit()

        return updated_order, HTTPStatus.OK

 
    @jwt_required()
    @order_namespace.doc(
        description = 'Delete an order using its id',
        params = {
        'order_id' : 'An ID for a given order'
        }
        )
    @order_namespace.marshal_with(order_model)
    def delete(self, order_id):
        """Deletes an order using its id"""

        order_to_delete = Orders.get_by_id(order_id)

        order_to_delete.delete()

    

        return order_to_delete, HTTPStatus.NO_CONTENT



@order_namespace.route('/user/<int:user_id>/orders')
class GetAllUserOrders(Resource):
    @order_namespace.doc(
            description = 'Get all orders by a specific user',
            params = {
                'user_id' : 'An ID for a given user'
            }
            
            )
    @order_namespace.marshal_list_with(order_model)
    @jwt_required()
    def get(self, user_id):
        """Get all orders by a specific user"""
        user = User.get_by_id(user_id)

        order = user.orders
        
        return order, HTTPStatus.OK


@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderByUser(Resource):
    @order_namespace.doc(
            description = 'Get a specific order by a specific user',
            params = {
        'order_id' : 'An ID for a given order',
        'user_id' : 'An ID for a given user'
        }
            )
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self, user_id, order_id):
        """Get a specific order by a specific user"""
        user = User.get_by_id(user_id)

        order = Orders.query.filter_by(id=order_id).filter_by(user=user).first()

        return order, HTTPStatus.OK


@order_namespace.route('/orders/status/<int:order_id>')
class OrderStatus(Resource):
    @jwt_required()
    @order_namespace.doc(
        description = 'Update an order status given the order id',
        params = {
        'order_id' : 'An ID for a given order'
        }
            )
    @order_namespace.marshal_with(order_model)
    @order_namespace.expect(order_status_model)
    def patch(self, order_id):
        """Update an order's status"""

        updated_status = Orders.get_by_id(order_id)

        data = order_namespace.payload

        updated_status.status = data['order_status']

        db.session.commit()

        return updated_status, HTTPStatus.OK
