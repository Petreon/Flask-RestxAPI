# Flask-RestxAPI
Creating a REST API Project using Flask_RESTx and JWT authentication

## Initialize the server
- create an enviroment viariable with $ export FLASK_APP=api/
- initiate the server $ flask run --host=0.0.0.0 or python3 runserver.py


## Create an .env folder
- create variable SECRET_KEY= 
- generate an key with the python secrets module or anything that you want and create a key

## To create a database
the sqlite database will be created in config folder with th default paramaters
- $ flask shell
- db.create_all()
- 
# API ROUTES
when a JWT token is required we need to put in the headers, Authorization : value: Bearer token_id

- /auth/signup/ METHOD: POST, Register a new User
- /auth/login/ METHOD: POST, Login User
- /auth/refresh METHOD: POST, Get a new JWT token, need to have: header: Authorization , value: Bearer token_id
- /orders/ METHOD: GET , Get all orders , jwt token required
- /orders/ METHOD: POST , create a new post , jwt token required, minimun json required example {"quantity":1,
    "flavour":"RUM",
    "order_status":"PENDING",
    "size":"SMALL"}

## Database "diagram"
![diagram](https://github.com/Petreon/Flask-RestxAPI/raw/main/database_diagram.drawio.png)
