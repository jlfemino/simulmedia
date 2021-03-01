import pytest

from simulmedia.types.exceptions import InvalidLanguageException
from simulmedia.types.language import Language


class TestLanguage:
    # ================================================================================
    # __init__()
    # ================================================================================
    def test__init__missing_name(self):
        with pytest.raises(InvalidLanguageException) as e:
            Language(alpha_2='en', alpha_3='eng')
        assert 'name not specified' in str(e)

    def test__init__alpha2_missing(self):
        with pytest.raises(InvalidLanguageException) as e:
            Language(name='English', alpha_3='eng')
        assert 'alpha_2 not specified' in str(e)

    def test__init__alpha2_too_long(self):
        with pytest.raises(InvalidLanguageException) as e:
            Language(name='English', alpha_2='eng', alpha_3='eng')
        assert 'alpha_2 must be 2 characters' in str(e)

    def test__init__alpha2_too_short(self):
        with pytest.raises(InvalidLanguageException) as e:
            Language(name='English', alpha_2='e', alpha_3='eng')
        assert 'alpha_2 must be 2 characters' in str(e)

    def test__init__alpha3_missing(self):
        with pytest.raises(InvalidLanguageException) as e:
            Language(name='English', alpha_2='en')
        assert 'alpha_3 not specified' in str(e)

    def test__init__alpha3_too_long(self):
        with pytest.raises(InvalidLanguageException) as e:
            Language(name='English', alpha_2='en', alpha_3='engl')
        assert 'alpha_3 must be 3 characters' in str(e)

    def test__init__alpha3_too_short(self):
        with pytest.raises(InvalidLanguageException) as e:
            Language(name='English', alpha_2='en', alpha_3='en')
        assert 'alpha_3 must be 3 characters' in str(e)

    def test__init__happy_path(self):
        language1 = Language(name='English', alpha_2='en', alpha_3='eng')
        language2 = Language.get('en')
        
        assert language1 is not None
        assert language2 is not None
        assert language1.equals(language2)

    # ================================================================================
    # __repr__()
    # ================================================================================
    def test__repr__happy_path(self):
        language = Language(name='English', alpha_2='en', alpha_3='eng')
        assert language.__repr__() == 'en'

    # ================================================================================
    # equals()
    # ================================================================================
    def test__equals__name_differs(self):
        language1 = Language(name='English1', alpha_2='en', alpha_3='eng')
        language2 = Language(name='English2', alpha_2='en', alpha_3='eng')

        assert language1 is not None
        assert language2 is not None
        assert not language1.equals(language2)

    def test__equals__alpha2_differs(self):
        language1 = Language(name='English', alpha_2='en', alpha_3='eng')
        language2 = Language(name='English', alpha_2='ne', alpha_3='eng')

        assert language1 is not None
        assert language2 is not None
        assert not language1.equals(language2)

    def test__equals__alpha3_differs(self):
        language1 = Language(name='English', alpha_2='en', alpha_3='eng')
        language2 = Language(name='English', alpha_2='en', alpha_3='egn')

        assert language1 is not None
        assert language2 is not None
        assert not language1.equals(language2)

    def test__equals__happy_path(self):
        language1 = Language(name='English', alpha_2='en', alpha_3='eng')
        language2 = Language(name='ENGLISH', alpha_2='EN', alpha_3='ENG')

        assert language1 is not None
        assert language2 is not None
        assert language1.equals(language2)

    # ================================================================================
    # get()
    # ================================================================================
    def test__get__iso639_none(self):
        with pytest.raises(InvalidLanguageException) as e:
            Language.get(None)
        assert 'Language not specified' in str(e)

    def test__get__iso639_blank(self):
        with pytest.raises(InvalidLanguageException) as e:
            Language.get('')
        assert 'Length invalid' in str(e)

    def test__get__iso639_too_short(self):
        with pytest.raises(InvalidLanguageException) as e:
            Language.get('a')
        assert 'Length invalid' in str(e)

    def test__get__iso639_too_long(self):
        with pytest.raises(InvalidLanguageException) as e:
            Language.get('aaaa')
        assert 'Length invalid' in str(e)

    def test__get__iso639_not_found(self):
        with pytest.raises(InvalidLanguageException) as e:
            Language.get('xx')
        assert 'Language not found' in str(e)

    def test__get__iso639_happy_path(self):
        language = Language.get('zh')
        assert language.alpha_2 == 'zh'
        assert language.alpha_3 == 'zho'
        assert language.name == 'Chinese'
