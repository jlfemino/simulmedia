from flask import Blueprint, current_app, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from simulmedia.config import config_parser

SWAGGER_URL = '/api/docs'
API_URL = 'http://localhost:5000/spec'  # Our API url (can of course be a local resource)

swagger_ui_api = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Simulmedia demo"})
swagger_api = Blueprint('swagger_api2', __name__)


# ====================================================================================================
# API
# ====================================================================================================
@swagger_api.route("/spec")
def spec():
    swag = swagger(current_app)
    swag['info']['version'] = config_parser['SWAGGER']['INFO_VERSION']
    swag['info']['title'] = config_parser['SWAGGER']['INFO_TITLE']
    return jsonify(swag)
