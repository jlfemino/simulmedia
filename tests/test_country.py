import pytest

from simulmedia.country import Country
from simulmedia.exceptions import InvalidCountryException


class TestCountry:
    # ================================================================================
    # __init__()
    # ================================================================================
    def test__init__missing_name(self):
        with pytest.raises(InvalidCountryException) as e:
            Country(alpha_2='en', alpha_3='eng')
        assert 'name not specified' in str(e)

    def test__init__alpha2_missing(self):
        with pytest.raises(InvalidCountryException) as e:
            Country(name='English', alpha_3='eng')
        assert 'alpha_2 not specified' in str(e)

    def test__init__alpha2_too_long(self):
        with pytest.raises(InvalidCountryException) as e:
            Country(name='English', alpha_2='eng', alpha_3='eng')
        assert 'alpha_2 must be 2 characters' in str(e)

    def test__init__alpha2_too_short(self):
        with pytest.raises(InvalidCountryException) as e:
            Country(name='English', alpha_2='e', alpha_3='eng')
        assert 'alpha_2 must be 2 characters' in str(e)

    def test__init__alpha3_missing(self):
        with pytest.raises(InvalidCountryException) as e:
            Country(name='English', alpha_2='en')
        assert 'alpha_3 not specified' in str(e)

    def test__init__alpha3_too_long(self):
        with pytest.raises(InvalidCountryException) as e:
            Country(name='English', alpha_2='en', alpha_3='engl')
        assert 'alpha_3 must be 3 characters' in str(e)

    def test__init__alpha3_too_short(self):
        with pytest.raises(InvalidCountryException) as e:
            Country(name='English', alpha_2='en', alpha_3='en')
        assert 'alpha_3 must be 3 characters' in str(e)

    def test__init__happy_path(self):
        country1 = Country(name='United States', alpha_2='US', alpha_3='USA')
        country2 = Country.get('us')

        assert country1 is not None
        assert country2 is not None
        assert country1.equals(country2)

    # ================================================================================
    # __repr__()
    # ================================================================================
    def test__repr__happy_path(self):
        country = Country(name='United States', alpha_2='US', alpha_3='USA')
        assert country.__repr__() == 'US'

    # ================================================================================
    # equals()
    # ================================================================================
    def test__equals__name_differs(self):
        country1 = Country(name='United States1', alpha_2='US', alpha_3='USA')
        country2 = Country(name='United States2', alpha_2='US', alpha_3='USA')

        assert country1 is not None
        assert country2 is not None
        assert not country1.equals(country2)

    def test__equals__alpha2_differs(self):
        country1 = Country(name='United States', alpha_2='US', alpha_3='USA')
        country2 = Country(name='United States', alpha_2='SU', alpha_3='USA')

        assert country1 is not None
        assert country2 is not None
        assert not country1.equals(country2)

    def test__equals__alpha3_differs(self):
        country1 = Country(name='United States', alpha_2='US', alpha_3='USA')
        country2 = Country(name='United States', alpha_2='US', alpha_3='UAS')

        assert country1 is not None
        assert country2 is not None
        assert not country1.equals(country2)

    def test__equals__happy_path(self):
        country1 = Country(name='United States', alpha_2='US', alpha_3='USA')
        country2 = Country(name='united states', alpha_2='us', alpha_3='usa')

        assert country1 is not None
        assert country2 is not None
        assert country1.equals(country2)

    # ================================================================================
    # get()
    # ================================================================================
    def test__get__iso3166_none(self):
        with pytest.raises(InvalidCountryException) as e:
            Country.get(None)
        assert 'Country not specified' in str(e)

    def test__get__iso3166_blank(self):
        with pytest.raises(InvalidCountryException) as e:
            Country.get('')
        assert 'Length invalid' in str(e)

    def test__get__iso3166_too_short(self):
        with pytest.raises(InvalidCountryException) as e:
            Country.get('A')
        assert 'Length invalid' in str(e)

    def test__get__iso3166_too_long(self):
        with pytest.raises(InvalidCountryException) as e:
            Country.get('AAAA')
        assert 'Length invalid' in str(e)

    def test__get__iso3166_not_found(self):
        with pytest.raises(InvalidCountryException) as e:
            Country.get('XX')
        assert 'Country not found' in str(e)

    def test__get__iso3166_happy_path(self):
        country = Country.get('EE')
        assert country.alpha_2 == 'EE'
        assert country.alpha_3 == 'EST'
        assert country.name == 'Estonia'
