from flask_restx import Resource, Namespace

order_namespace = Namespace('orders', description="Namespace for orders")

@order_namespace.route('/')
class OrderGetCreate(Resource):

    def get(self):
        """ Get all orders"""

        return{"message":"getting orders"}

    def post(self):
        """ Place a new order"""
        return {"message":"posting orders"}


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
