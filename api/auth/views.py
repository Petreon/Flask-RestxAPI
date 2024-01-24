from flask_restx import Namespace, Resource, fields ## Namespace is similar to a blueprint
from flask import request
from ..models.users import User
from werkzeug.security import generate_password_hash , check_password_hash
from http import HTTPStatus
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, )

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

login_model = auth_namespace.model(
    'Login',{
        'email': fields.String(required = True, description = "An email"),
        'password': fields.String(required = True, description = "A password")
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

    @auth_namespace.expect(login_model)
    def post(self):
        """ Generate a JWT pair """

        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password_hash, password):
            # create the token specified for the user
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)

            response = {
                'access_token':access_token,
                'refresh_token':refresh_token
            }

            return response, HTTPStatus.OK
        
        return {"message":"User Not Found"}


@auth_namespace.route('/refresh')
class Refresh(Resource):

    @jwt_required(refresh=True) # only can get the refresh token so we send a new refresh token too
    def post(self):
        # get the unique username from the user, have another ways to do this in the documentation
        username = get_jwt_identity() ## i dont know what this try to access but

        access_token = create_access_token(identity = username)
        refresh_token = create_refresh_token(identity = username)

        return {'access_token':access_token, 'refresh_token':refresh_token}, HTTPStatus.OK