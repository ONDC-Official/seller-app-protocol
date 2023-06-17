import os

from flask_cors import CORS

from main.flask_app import app
from main.models.init_database import init_database
from main.routes import api


def create_tables():
    init_database(False)


api.init_app(app)
CORS(app)
create_tables()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if __name__ == "__main__":
    if os.getenv("ENV") is not None:
        # flask_s3.create_all(app)
        app.run(host="0.0.0.0", port=app.config["PORT"])
