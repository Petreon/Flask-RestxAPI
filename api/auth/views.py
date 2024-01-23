from flask_restx import Namespace, Resource ## is similar to a blueprint

## creating a namespace "blueprint"
auth_namespace = Namespace('auth', description="a namesoace for authentication")


@auth_namespace.route('/signup') ## create a route /auth
class SignUp(Resource):

    def post(self):
        """ Create a new User """
        pass


@auth_namespace.route('/login')
class login(Resource):

    def post(self):
        """ Generate a JWT pair """
        pass