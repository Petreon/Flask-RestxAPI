from api import create_app

app = create_app()

# the debug works here because we are in the same path as .env so the .config classes will work now

if __name__ == "__main__":
    #print(f"{app.config['HOST']}")
    app.run(host="0.0.0.0")