from flask_restx import Resource, Namespace, fields, reqparse
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.orders import Order
from ..models.users import User
from http import HTTPStatus
from ..utils import db

order_namespace = Namespace('orders', description="Namespace for orders")

orders_model = order_namespace.model(
    'Order',{
        'id': fields.Integer(description = "An Order ID", required=True),
        'size': fields.String(description = "Size of order", required=True, enum=['SMALL','MEDIUM','LARGE','EXTRA_LARGE']),
        'order_status': fields.String(description = " The status of the Order", required = True, enum=['PENDING','IN_TRANSIT','DELIVERED']),
        'flavor':fields.String(description="The pizza flavour", required = True),
        'quantity': fields.Integer(description = "Order Quantity", required = True)

    }
)

# creating an order parser to give an error if the request is not passed as expected
order_parser = reqparse.RequestParser()
order_parser.add_argument('size', type=str, required=True, help='Size of order', choices=['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE'])
order_parser.add_argument('order_status', type=str, required=False, help='The status of the Order', choices=['PENDING', 'IN_TRANSIT', 'DELIVERED'])
order_parser.add_argument('flavour', type=str, required=True, help='The pizza flavour')
order_parser.add_argument('quantity', type=int, required=True, help='The pizza flavour')


order_status_model = order_namespace.model(
    'OrderStatus', {
        'order_status': fields.String(required=True, description = "Order status", enum=['PENDING','IN_TRANSIT','DELIVERED'])
    }
)

order_status_parser = reqparse.RequestParser()
order_status_parser.add_argument('order_status', type=str, required=True, choices=['PENDING', 'IN_TRANSIT', 'DELIVERED'])


@order_namespace.route('/')
class OrderGetCreate(Resource):

    @order_namespace.marshal_with(orders_model)
    @order_namespace.doc(
        description="Retrieve all Orders"
    )
    @jwt_required()
    def get(self):
        """ Get all orders"""

        orders = Order.query.all()

        return orders , HTTPStatus.OK


    @order_namespace.expect(order_parser)
    @order_namespace.marshal_with(orders_model)
    @order_namespace.doc(
        description="Place an Order"
    )
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

    @order_namespace.marshal_with(orders_model)
    @order_namespace.doc(
        description="Retrieve an order by order_id"
    )
    @jwt_required()
    def get(self,order_id):
        """ Retrieve an order by id """

        # i didn't like this manner but its ok
        order = Order.get_by_id(order_id)

        return order , HTTPStatus.OK
    
    @order_namespace.expect(order_parser)
    @order_namespace.doc(
        description="Update an Order giving all needed parameters"
    )
    @jwt_required()
    def put(self,order_id):
        ## needs to implement if the order id can be modified for this user
        """ Update an Order needs to pass all the required fields"""

        order_to_update = Order.query.filter_by(id = order_id).first()

        new_data_order = order_parser.parse_args()

        order_to_update.quantity = new_data_order['quantity']
        order_to_update.size = new_data_order['size']
        order_to_update.flavor = new_data_order['flavour']

        if new_data_order['order_status'] is not None:
            order_to_update.order_status = new_data_order['order_status']

        db.session.commit()

        return order_namespace.marshal(order_to_update,orders_model), HTTPStatus.OK
        
    @jwt_required()
    @order_namespace.doc(
        description="Delete a order given an order id, needs jwt token"
    )
    def delete(self,order_id):
        """ Delete a Order """

        order_to_delete = Order.query.filter_by(id = order_id).first()

        if order_to_delete is not None:
            db.session.delete(order_to_delete)
            db.session.commit()
            return {"message": f"Order {order_id} deleted"}, HTTPStatus.OK

        return {"message": f"Order {order_id} Not found"}, 404


@order_namespace.route("/<int:order_id>/user/<int:user_id>")
class GetOrderByUser(Resource):

    @order_namespace.doc(
        description="Get a user specific Order"
    )
    @jwt_required()
    def get(self,order_id,user_id):
        """ Get a user specific order """

        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return {"message": "user not Found"}, 404
        if user.username != get_jwt_identity():
            return {"message": "cannot access another User order"}, HTTPStatus.UNAUTHORIZED
        
        ## this query is to get the order id from the user id
        order = Order.query.filter(Order.id == order_id, Order.user == user.id).first()

        return order_namespace.marshal(order,orders_model)


@order_namespace.route("/user/<int:user_id>")
class UserOrders(Resource):
    
    @order_namespace.doc(
        description="Retrieve all user Orders"
    )
    @jwt_required()
    def get(self, user_id):
        """Get all orders by a specific user"""
        
        user = User.query.filter_by(id=user_id).first()
        jwt_username = get_jwt_identity()

        if not user:
            #print("ACHIEVED")
            return {"message":"User not found"}, HTTPStatus.NOT_FOUND
        if user.username != jwt_username:
            #print("ACHIEVED")
            return {"message": "User Not allowed to retrives orders from another User"}, 401
        
        ## is like a join
        orders = user.orders
        if not orders:
            return {"message": "User dont have any orders"}, 401
        
        #changing the way that we do the marshal because we need to return error to handle authentication
        return order_namespace.marshal(orders,orders_model), HTTPStatus.OK


@order_namespace.route('/status/<int:order_id>')
class UpdateOrderStatus(Resource):

    @order_namespace.doc(
        description="Update an order Status given the order Id"
    )
    @order_namespace.expect(order_status_parser)
    @jwt_required()
    def patch(self,order_id):
        """Update an order's status"""
        # getting the data from the request
        data = order_status_parser.parse_args()

        order_to_update = Order.query.filter_by(id=order_id).first()

        if order_to_update is None:
            return {"message": f"Order Id = {order_id} doesn't exists"}, HTTPStatus.NOT_FOUND
        
        order_to_update.order_status = data['order_status']
        db.session.commit()

        return order_namespace.marshal(order_to_update, orders_model), HTTPStatus.OK

