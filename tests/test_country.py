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


