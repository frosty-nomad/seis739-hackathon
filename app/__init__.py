import os

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from .api import api_bp
from .extensions import db
from .web import web_bp


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'app.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(web_bp)

    swagger_bp = get_swaggerui_blueprint(
        "/docs",
        "/static/openapi.json",
        config={"app_name": "Party Guest List API"},
    )
    app.register_blueprint(swagger_bp, url_prefix="/docs")

    return app
