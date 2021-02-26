import pytest

from simulmedia.exceptions import InvalidInputException
from simulmedia.validate import Validate


class TestValidate:
    # ================================================================================
    # validate_country_iso_639_2()
    # ================================================================================
    def test__validate_country__invalid_country__none(self):
        with pytest.raises(InvalidInputException) as e:
            Validate.validate_country_iso_639_2(None)
        assert 'Country not specified' in str(e)

    def test__validate_country__invalid_country__empty(self):
        with pytest.raises(InvalidInputException) as e:
            Validate.validate_country_iso_639_2('')
        assert 'Country not specified' in str(e)

    def test__validate_country__invalid_country__too_long(self):
        with pytest.raises(InvalidInputException) as e:
            Validate.validate_country_iso_639_2('USA')
        assert 'Country length invalid' in str(e)

    def test__validate_country__invalid_country__too_short(self):
        with pytest.raises(InvalidInputException) as e:
            Validate.validate_country_iso_639_2('U')
        assert 'Country length invalid' in str(e)

    def test__validate_country__invalid_country__not_found(self):
        with pytest.raises(InvalidInputException) as e:
            Validate.validate_country_iso_639_2('xx')
        assert 'Country not found' in str(e)

    # ================================================================================
    # validate_hour()
    # ================================================================================
    def test__validate_hour__invalid_hour__none(self):
        with pytest.raises(InvalidInputException) as e:
            Validate.validate_hour(None)
        assert 'Hour not specified' in str(e)

    def test__validate_hour__invalid_hour__too_small(self):
        with pytest.raises(InvalidInputException) as e:
            Validate.validate_hour(-1)
        assert 'Hour out of range' in str(e)

    def test__validate_hour__invalid_hour__too_large(self):
        with pytest.raises(InvalidInputException) as e:
            Validate.validate_hour(25)
        assert 'Hour out of range' in str(e)
