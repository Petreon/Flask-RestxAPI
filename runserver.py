from api import create_app
from api.config.config import config_dict
from dotenv import load_dotenv
import os

load_dotenv()

string_prod = os.getenv('CONFIG_STATE')

if string_prod == "prod":
    app = create_app(config=config_dict['prod'])
else:
    app = create_app()


# the debug works here because we are in the same path as .env so the .config classes will work now

if __name__ == "__main__":
    #print(f"{app.config['HOST']}")
    app.run(host="0.0.0.0")