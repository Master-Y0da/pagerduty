from flask import Flask
from .routes.v1 import v1


def create_app() -> Flask:
    
    app = Flask(__name__)
    app.register_blueprint(v1, url_prefix='/api/v1')   

    return app
