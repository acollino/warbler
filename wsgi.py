from app import init_app

app = init_app(".env")

if __name__ == "__main__":
    app.run()
