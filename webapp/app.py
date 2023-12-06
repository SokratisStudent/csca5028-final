from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__, template_folder='html')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vacations.sqlite3'

    return app
