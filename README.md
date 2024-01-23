# Flask-RestxAPI
Creating a REST API Project using Flask_RESTx and JWT authentication

## Initialize the server
- create an enviroment viariable with $ export FLASK_APP=api/
- initiate the server $ flask run --host=0.0.0.0 or python3 runserver.py


## create an .env folder
- create variable SECRET_KEY= 
- generate an key with the python secrets module or anything that you want and create a key

# API ROUTES
- /auth/signup/ METHOD: POST, Register a new User
- /auth/login/ METHOD: POST, Login User