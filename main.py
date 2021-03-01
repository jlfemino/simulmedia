import os

from flask import Flask

from simulmedia.api.ad_api import ad_api_blueprint
from simulmedia.api.swagger_api import swagger_api_blueprint, swagger_ui_api_blueprint
from simulmedia.services.config import config_parser
from simulmedia.services.database import apply_db_migrations
from simulmedia.types.exceptions import ConfigException
from simulmedia.services.ads_fetcher import AdsFetcher

# Flask app
app = Flask(__name__)
app.register_blueprint(swagger_api_blueprint)
app.register_blueprint(swagger_ui_api_blueprint)
app.register_blueprint(ad_api_blueprint)

# ====================================================================================================
# Main
# ====================================================================================================
if __name__ == '__main__':
    if not os.environ.get('APP_ENV', None):
        raise ConfigException('APP_ENV not defined!')

    apply_db_migrations()

    url = config_parser['DEFAULT']['AD_CONFIGS_URL']
    AdsFetcher.get_instance().fetch_ads(url=url)

    app.run()
