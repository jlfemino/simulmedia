
from simulmedia.exceptions import InvalidInputException
import pycountry


class Validate:
    @staticmethod
    def validate_country_iso_639_2(country: str):
        if not country:
            raise InvalidInputException(f'Country not specified. Use ISO 639-2 format. country={country}')

        if len(country) != 2:
            raise InvalidInputException(f'Country length invalid. Use ISO 639-2 format. country={country}')

        if pycountry.countries.get(alpha_2=country) is None:
            raise InvalidInputException(f'Country not found for ISO 639-2 code={country}')

    @staticmethod
    def validate_language_iso_639(lang: str):
        if not lang:
            raise InvalidInputException(f'Language not specified. lang={lang}')

        if len(lang) == 2:
            language = pycountry.languages.get(alpha_2=lang)
        elif len(lang) == 3:
            language = pycountry.languages.get(alpha_3=lang)
        else:
            raise InvalidInputException(f'Language length invalid. Use ISO 639-1 or ISO 639-2/T format. lang={lang}')

        if language is None:
            raise InvalidInputException(f'Language not found for ISO 639 code={lang}')

        return language

    @staticmethod
    def validate_hour(hour: int):
        if hour is None:
            raise InvalidInputException(f'Hour not specified. Use [0..23] in UTC.')

        if hour < 0 or hour > 23:
            raise InvalidInputException(f'Hour out of range. Use [0..23] in UTC. hour={hour}')

