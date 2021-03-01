import json
import logging
from datetime import datetime
from typing import Optional, Union

from flask import Blueprint, make_response

from simulmedia.dao.user_dao import UserDao
from simulmedia.services.ads_fetcher import AdsFetcher
from simulmedia.services.config import config_parser
from simulmedia.types.ad import Ad
from simulmedia.types.country import Country
from simulmedia.types.exceptions import InvalidInputException
from simulmedia.types.language import Language
from simulmedia.types.user import User

_logger = logging.getLogger(__name__)

default_headers = json.loads(config_parser['DEFAULT']['DEFAULT_HEADERS'])

ad_api_blueprint = Blueprint('ad_api', __name__)


@ad_api_blueprint.route('/ad/<user_id>/<country>/<language>')
def get_ad_url_short(user_id: str, country: str, language: str) -> Optional[Ad]:
    """
    Get video ad URL based on country and language.
    ---
    parameters:
        - name: user_id
          in: path
          type: string
          required: true
          description: ID of User. Non-negotiable.
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
            description: No ad was found for the specified user/country/language
    """
    return get_ad_url(user_id=user_id, country=country, language=language, hour=datetime.utcnow().hour)


@ad_api_blueprint.route('/ad/<user_id>/<country>/<language>/<hour>')
def get_ad_url(user_id: str,
               country: str,
               language: str,
               hour: Union[str, int] = None) -> Optional[Ad]:
    """
    Get video ad URL based on country, language, and hour.
    ---
    parameters:
        - name: user_id
          in: path
          type: string
          required: true
          description: ID of User. Non-negotiable.
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
            description: No ad was found for the specified user/country/language/hour
    """
    response = make_response()
    response.headers.update(default_headers)
    try:
        # Process input args
        u: Optional[User] = UserDao.get_instance().get_by_id(user_id)
        if u is None:
            raise InvalidInputException(f'User not found for user_id={user_id}')

        c: Country = Country.get(country)
        l: Language = Language.get(language)
        h: int = int(hour)
        ad = AdsFetcher.get_instance().determine_ad_for_user(u, c, l, h)

        if ad:
            response.status_code = 200
            response.data = ad.video_url
        else:
            response.status_code = 404
    except InvalidInputException as e:
        response.status_code = 400
        response.data = str(e)
    except Exception as e:
        response.status_code = 500
        response.data = str(e)

    return response
