import os


def prod_config():
    return {
        # "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:root@localhost/taskmanagement",
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{os.path.dirname(os.path.realpath(__file__))}/database/db.sqlite",
        "CORS": [
            "http://ec2-54-252-152-168.ap-southeast-2.compute.amazonaws.com",
            "http://localhost:8080",
            "http://127.0.0.1:5000",
        ],
        "JWT_SECRET_KEY": "#ABCDEFGHIJK#",
        "PORT": 80,
        "static_url_path": "/",
        "static_folder": "frontend/dist/spa",
    }


def dev_config():
    return {
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{os.path.dirname(os.path.realpath(__file__))}/database/db.sqlite",
        "CORS": ["http://localhost:8080", "http://127.0.0.1:5000"],
        "JWT_SECRET_KEY": "#ABCDEFGHIJK#",
        "PORT": 5000,
        "static_url_path": "/",
        "static_folder": "frontend/dist/spa",
        "static_url_path": "/",
        "static_folder": "statics",
    }


def is_production_mode():
    return "ENV" in os.environ and os.environ["ENV"] == "PRODUCTION"


def get_config():
    if is_production_mode():
        return prod_config()
    else:
        return dev_config()
