from flask_restx import Namespace, Resource, fields ## Namespace is similar to a blueprint
from flask import request
from ..models.users import User
from werkzeug.security import generate_password_hash , check_password_hash
from http import HTTPStatus

## creating a namespace "blueprint"
auth_namespace = Namespace('auth', description="a namesoace for authentication")

#serialize the module i could use the reqparse instead of this
signup_model = auth_namespace.model(
    'SignUp',{
        'id':fields.Integer(),
        'username':fields.String(required=True, description="A username"),
        'email':fields.String(required=True, description="A email"),
        'password':fields.String(required=True, description="A password"),
    }
)

user_model = auth_namespace.model(
    'User',{
        'id':fields.Integer(),
        'username':fields.String(required=True, description="A username"),
        'email':fields.String(required=True, description="A email"),
        'password':fields.String(required=True, description="A password"),
        'is_active': fields.Boolean(description="This shows that User is active"),
        'is_staff':fields.Boolean(description="this shows of use is staff")
    }
)


@auth_namespace.route('/signup') ## create a route /auth
class SignUp(Resource):

    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model) ## return the user with the model that we created before
    def post(self):
        """ Create a new User """
        data = request.get_json()
        ## data is a dictionary that i can retrieve with .get() method
        new_user = User(
            username = data.get('username'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password'))
        )

        new_user.save() ## save the user in the database

        return new_user , HTTPStatus.CREATED






@auth_namespace.route('/login')
class login(Resource):

    def post(self):
        """ Generate a JWT pair """
        pass