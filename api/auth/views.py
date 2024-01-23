from flask_restx import Namespace, Resource ## is similar to a blueprint

## creating a namespace "blueprint"
auth_namespace = Namespace('auth', description="a namesoace for authentication")


@auth_namespace.route('/') ## create a route /auth
class HelloAuth(Resource):

    def get(self):
        return {"message": "hello Auth"}
