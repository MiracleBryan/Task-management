""" Backend Module """

""" Application Init """
from flask import Flask, redirect
from flask_cors import CORS

from database.models import init_app_database
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

from config import get_config, is_production_mode

cfg = get_config()

app = Flask(
    __name__, static_folder=cfg["static_folder"], static_url_path=cfg["static_url_path"]
)

app.config["SQLALCHEMY_DATABASE_URI"] = cfg["SQLALCHEMY_DATABASE_URI"]
""" CORS """
CORS(
    app, origins=cfg["CORS"], supports_credentials=True
)  # TODO: Move to a config file. Add aws / production origins here.

""" JWT """
app.config["JWT_SECRET_KEY"] = cfg["JWT_SECRET_KEY"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
jwt = JWTManager(app)

""" Database Init """
init_app_database(app, True)

""" Socket """
socketapp = SocketIO(
    app, cors_allowed_origins=cfg["CORS"], debug=True, logger=True
)  # , engineio_logger=True) PingPongs

""" API """
api_prefix = "/api"

if is_production_mode():  # Quasar in production.

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def frontend(path):
        return app.send_static_file("index.html")

else:  # Swagger in development.

    @app.route("/")
    def swagger_doc():
        return app.redirect(f"http://localhost:{cfg['PORT']}{api_prefix}")


from api import blueprint as api_blueprint

app.register_blueprint(api_blueprint, url_prefix=api_prefix)
app.debug = True
