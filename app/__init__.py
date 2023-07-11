from config import Config

from flask import Flask

from . import routes


app = Flask(__name__)
with app.app_context():
    app.config.from_object(Config)
    app.register_blueprint(routes.app)
