from flask import Flask

def create_app():
    # using a function factory to create the app
    app = Flask(__name__)

    return app