# Flask-RestxAPI
Creating a REST API Project using Flask_RESTx and JWT authentication
its an simple Pizza Orders API, that you can create an user, create orders for pizza like flavour, quantity and see the order_status

## Initialize the server
- create an enviroment viariable with $ export FLASK_APP=api/
- initiate the server $ flask run --host=0.0.0.0 or python3 runserver.py (recommended)


## Create an .env folder
- create variable SECRET_KEY= 
- generate an key with the python secrets module or anything that you want and create a key

## To create a database
the sqlite database will be created in config folder using the default paramaters
- $ flask shell
- db.create_all()

## Run Tests
only need to run pytest in the root folder
- $ pytest

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
- /orders/<int:id>: METHOD: GET, get the order with id , jwt token required
- /orders/<int:id>: METHOD: PUT, alterate the order with order_id , jwt token required and require the minimum json
- /orders/<int:id>: METHOD: DELETE, Delete the order, jwt token is required
- /orders/user/<int:id>: METHOD: GET, get the all user specific orders, jwt token from user required
- /orders/<int:order_id>/user/<int:user_id>: METHOD: GET, get a specific order from specific user, jwt token required
- /orders/status/<int:order_id>: METHOD: PATCH, update the status code from the order, jwt token required


## Database "diagram"
![diagram](https://github.com/Petreon/Flask-RestxAPI/raw/main/database_diagram.drawio.png)
