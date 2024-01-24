from flask_restx import Resource, Namespace, fields, reqparse
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.orders import Order
from ..models.users import User
from http import HTTPStatus

order_namespace = Namespace('orders', description="Namespace for orders")

orders_model = order_namespace.model(
    'Order',{
        'id': fields.Integer(description = "An Order ID"),
        'size': fields.String(description = "Size of order", required=True, enum=['SMALL','MEDIUM','LARGE','EXTRA_LARGE']),
        'order_status': fields.String(description = " The status of the Order", required = True, enum=['PENDING','IN-TRANSIT','DELIVERED']),
        'flavor':fields.String(description="The pizza flavour", required = True),
        'quantity': fields.Integer(description = "Order Quantity", required = True)

    }
)

order_parser = reqparse.RequestParser()
order_parser.add_argument('size', type=str, required=True, help='Size of order', choices=['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE'])
order_parser.add_argument('order_status', type=str, required=True, help='The status of the Order', choices=['PENDING', 'IN-TRANSIT', 'DELIVERED'])
order_parser.add_argument('flavour', type=str, required=True, help='The pizza flavour')
order_parser.add_argument('quantity', type=int, required=True, help='The pizza flavour')


@order_namespace.route('/')
class OrderGetCreate(Resource):

    @order_namespace.marshal_with(orders_model)
    @jwt_required()
    def get(self):
        """ Get all orders"""

        orders = Order.query.all()

        return orders , HTTPStatus.OK


    @order_namespace.expect(order_parser)
    @order_namespace.marshal_with(orders_model)
    @jwt_required()
    def post(self):
        """ Place a new order"""

        data = order_parser.parse_args()

        ## accessing extra fields not defined in the parser
        extra_fields = {key: value for key, value in request.json.items() if key not in data}

        final_data = data.copy()
        final_data.update(extra_fields)

        if data is not None:
            new_order = Order(
                size = data['size'],
                quantity = data['quantity'],
                flavor = data['flavour'], #unfortunetily an mispelling in the database
                order_status = data['order_status']
            )

            # is not an optimised way to do this because dont have an index for usernames in the database
            username = get_jwt_identity()

            user = User.query.filter_by(username=username).first()
            if user is not None:
                new_order.user = user.id
                new_order.save()

        return new_order , HTTPStatus.CREATED





@order_namespace.route('/<int:order_id>')
class OrderUpdateDelete(Resource):

    def get(self,order_id):
        """ Retrieve an order by id """
        return {"message":f"getting the order {order_id}"}
    
    def put(self,order_id):
        """ Update an Order """
        return {"message": f"Order {order_id} updated"}
    
    def delete(self,order_id):
        """ Delete a Order """
        return {"message": f"Order {order_id} deleted"}


@order_namespace.route("/<int:order_id>/user/<int:user_id>")
class GetOrderByUser(Resource):

    def get(self,order_id,user_id):
        """ Get a user specific order """
        pass


@order_namespace.route("/user/<int:user_id>")
class UserOrders(Resource):

    def get(self, user_id):
        """Get all orders by a specific user"""
        pass


@order_namespace.route('/status/<int:order_id>')
class UpdateOrderStatus(Resource):

    def patch(self,order_id):
        """Update an order's status"""
        pass
