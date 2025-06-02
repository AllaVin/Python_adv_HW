from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from .models import db
from .routes import api

load_dotenv()  # загружаем .env
app = Flask(__name__, instance_relative_config=True)

import os

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'av_questionnaire.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(api)

if __name__ == '__main__':
    app.run()

