from flask import Flask
from flask_restx import Api
from .orders.views import order_namespace
from .auth.views import auth_namespace
from .config.config import config_dict
from .utils import db
from .models.orders import Order
from .models.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed


def create_app(config=config_dict['dev']):
    # using a function factory to create the app
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app,db)

    # create an authorization jwt to use the swagger
    authorizations = {
        "Bearer Auth":{
            'type':'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description':'Add a JWT with ** Bearer &lt;JWT&gt; to authorize'
        }
    }

    api = Api(app, title="Pizza Delivery API",
              description="A REST API for a Pizza Delivery Service",
              authorizations=authorizations,
              security="Bearer Auth")

    api.add_namespace(order_namespace)
    api.add_namespace(auth_namespace)

    jwt = JWTManager(app) ## instantiate the jwt manager into application


    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, 404
    
    @api.errorhandler(MethodNotAllowed)
    def Method_not_allowed(error):
        return {"error": "Method not Allowed"},405

    ## something that i can call the database in the shell to instantiate
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db':db,
            'User':User,
            'Order':Order
        }

    return app