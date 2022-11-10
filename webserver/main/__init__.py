import os


def create_app(config_name):
    from flask import Flask
    from main.config import config_by_name

    app = Flask(__name__, template_folder='templates', static_url_path='')
    app.config.from_object(config_by_name[config_name])
    app.app_context().push()
    return app


app = create_app(os.getenv("ENV") or "dev")
