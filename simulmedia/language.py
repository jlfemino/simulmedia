import pycountry

from simulmedia.exceptions import InvalidLanguageException


# TODO: Internationalize this by including the ability to fetch internationalized name


class Language:
    """
    A wrapper on top of pycountry, to provide the ability to get Language objects from ISO 639-1 & 639-2/T codes.
    """
    name: str = None
    alpha_2: str = None
    alpha_3: str = None

    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']

        if 'alpha_2' in kwargs:
            if len(kwargs['alpha_2']) != 2:
                raise InvalidLanguageException(f'alpha_2 must be 2 characters: {kwargs["alpha_2"]}')
            self.alpha_2 = kwargs['alpha_2']

        if 'alpha_3' in kwargs:
            if len(kwargs['alpha_3']) != 3:
                raise InvalidLanguageException(f'alpha_3 must be 3 characters: {kwargs["alpha_3"]}')
            self.alpha_3 = kwargs['alpha_3']

        # Ensure that all required attributes are set
        for field in ['name', 'alpha_2', 'alpha_3']:
            if getattr(self, field) is None:
                raise InvalidLanguageException(f'{field} not specified')

    def __repr__(self):
        return self.alpha_2

    @classmethod
    def get(cls, iso639: str):
        if iso639 is None:
            raise InvalidLanguageException(f'Language not specified. Use ISO 639-1 or ISO 639-2/T code.')

        if len(iso639) == 2:
            pyc_lang = pycountry.languages.get(alpha_2=iso639)
        elif len(iso639) == 3:
            pyc_lang = pycountry.languages.get(alpha_3=iso639)
        else:
            raise InvalidLanguageException(f'Length invalid. Use ISO 639-1 or ISO 639-2/T format. iso639={iso639}')

        if pyc_lang is None:
            # TODO: Use a more comprehensive library... and consider using a cache
            for lang in pycountry.languages:
                if hasattr(lang, 'bibliographic') and lang.bibliographic == iso639:
                    pyc_lang = lang
                    break

        if pyc_lang is None:
            raise InvalidLanguageException(f'Language not found for ISO 639 code={iso639}.')

        return Language(name=pyc_lang.name, alpha_2=pyc_lang.alpha_2, alpha_3=pyc_lang.alpha_3)

    def equals(self, other: 'Language') -> bool:
        return self.name.lower() == other.name.lower() \
               and self.alpha_2.lower() == other.alpha_2.lower() \
               and self.alpha_3.lower() == other.alpha_3.lower()
