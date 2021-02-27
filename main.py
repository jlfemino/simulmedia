from flask import Flask

from simulmedia.api.ad import ad_api
from simulmedia.api.swagger import swagger_api, swagger_ui_api
from simulmedia.database import apply_db_migrations

# Flask app
app = Flask(__name__)
app.register_blueprint(swagger_api)
app.register_blueprint(swagger_ui_api)
app.register_blueprint(ad_api)


# ====================================================================================================
# Main
# ====================================================================================================
if __name__ == '__main__':
    apply_db_migrations()
    app.run()
