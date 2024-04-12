import os

from flask_cors import CORS

from main.flask_app import app
from main.routes import api


api.init_app(app)
CORS(app)

if __name__ == "__main__":
    if os.getenv("ENV") is not None:
        # flask_s3.create_all(app)
        app.run(host="0.0.0.0", port=app.config["PORT"])
