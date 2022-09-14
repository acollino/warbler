from app import init_app

# change to ProdConfig before deploying
app = init_app("config.DevConfig")

if __name__ == "__main__":
    app.run()
