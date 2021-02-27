import json
import logging
from datetime import datetime
from typing import Optional, Union

from flask import Blueprint, make_response

from simulmedia.ad_config import AdConfig, AdConfigs
from simulmedia.config import config_parser
from simulmedia.country import Country
from simulmedia.exceptions import InvalidInputException
from simulmedia.language import Language

_logger = logging.getLogger(__name__)

default_headers = json.loads(config_parser['DEFAULT']['DEFAULT_HEADERS'])

# Load ad configs  # TODO: Could have listener service where config can be pushed to
url = config_parser['DEFAULT']['AD_CONFIGS_URL']
default_ad_configs: Optional[AdConfigs] = AdConfigs.fetch_ad_configs(url)


ad_api = Blueprint('swagger_api', __name__)


# ====================================================================================================
# API
# ====================================================================================================
@ad_api.route('/ad/<country>/<language>')
def get_ad_url_short(country: str, language: str) -> Optional[AdConfig]:
    """
    Get video ad URL based on country and language.
    ---
    parameters:
        - name: country
          in: path
          type: string
          required: true
          description: ISO 3166-1 Alpha-2 (2-char) or Alpha-3 (3-char) format country code.
            https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
        - name: language
          in: path
          type: string
          required: true
          description: ISO 639-1 (2-char) or 639-2/T (3-char) format language code.
            https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    responses:
        200:
            description: An ad video was found, and returned in response
        404:
            description: No ad was found for the specified country/language/hour
    """
    return get_ad_url(country=country, language=language, hour=datetime.utcnow().hour)


@ad_api.route('/ad/<country>/<language>/<hour>')
def get_ad_url(country: str,
               language: str,
               hour: Union[str, int] = None,
               ad_configs: AdConfigs = default_ad_configs) -> Optional[AdConfig]:
    """
    Get video ad URL based on country, language, and hour.
    ---
    parameters:
        - name: country
          in: path
          type: string
          required: true
          description: ISO 3166-1 Alpha-2 (2-char) or Alpha-3 (3-char) format country code.
            https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
        - name: language
          in: path
          type: string
          required: true
          description: ISO 639-1 (2-char) or 639-2/T (3-char) format language code.
            https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
        - name: hour
          in: path
          type: int
          required: false
          description: Integer [0-23] representing the hour of day in which ad is to be served, in UTC.
    responses:
        200:
            description: An ad video was found, and returned in response
        404:
            description: No ad was found for the specified country/language/hour
    """
    response = make_response()
    response.headers.update(default_headers)
    try:
        # Process input args
        c: Country = Country.get(country)
        l: Language = Language.get(language)
        h: int = int(hour)
        ad_config = ad_configs.get_ad(c, l, h)

        if ad_config:
            response.status_code = 200
            response.data = ad_config.video_url
        else:
            response.status_code = 404
    except InvalidInputException as e:
        response.status_code = 400
        response.data = str(e)

    return response
