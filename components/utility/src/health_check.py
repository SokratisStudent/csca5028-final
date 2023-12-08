from flask import Blueprint

root_blueprint = Blueprint('root', __name__)


@root_blueprint.route('/health')
def health_check():
    return {'message': 'Healthy'}
