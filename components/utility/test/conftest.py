import pytest

from flask import Flask
from components.utility.src.health_check import root_blueprint


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__, template_folder='../html')
    app.register_blueprint(root_blueprint)

    return app
