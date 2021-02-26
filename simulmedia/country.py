from simulmedia.exceptions import InvalidCountryException
import pycountry


class Country:
    name: str = None
    official_name: str = None
    alpha_2: str = None
    alpha_3: str = None

    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']
            self.official_name = kwargs['name']  # In case there is no "official_name"

        if 'official_name' in kwargs:
            self.official_name = kwargs['official_name']

        if 'alpha_2' in kwargs:
            if len(kwargs['alpha_2']) != 2:
                raise InvalidCountryException(f'alpha_2 must be 2 characters: {kwargs["alpha_2"]}')
            self.alpha_2 = kwargs['alpha_2']

        if 'alpha_3' in kwargs:
            if len(kwargs['alpha_3']) != 3:
                raise InvalidCountryException(f'alpha_3 must be 3 characters: {kwargs["alpha_3"]}')
            self.alpha_3 = kwargs['alpha_3']

        # Ensure that all required attributes are set
        for field in ['name', 'alpha_2', 'alpha_3']:
            if getattr(self, field) is None:
                raise InvalidCountryException(f'{field} not specified')

    def __repr__(self):
        return self.alpha_2

    @classmethod
    def get(cls, iso639: str):
        if len(iso639) == 2:
            pyc_country = pycountry.countries.get(alpha_2=iso639)
        elif len(iso639) == 3:
            pyc_country = pycountry.countries.get(alpha_3=iso639)
        else:
            raise InvalidCountryException(f'Length invalid. Use ISO 639-1 or ISO 639-2/T format. iso639={iso639}')

        if pyc_country is None:
            raise InvalidCountryException(f'Country not found for ISO 639 code={iso639}')

        return Country(
            name=pyc_country.name,
            official_name=getattr(pyc_country, 'official_name', pyc_country.name),
            alpha_2=pyc_country.alpha_2,
            alpha_3=pyc_country.alpha_3)

    def equals(self, other: 'Country') -> bool:
        return self.name.upper() == other.name.upper() \
               and self.alpha_2.upper() == other.alpha_2.upper() \
               and self.alpha_3.upper() == other.alpha_3.upper()
