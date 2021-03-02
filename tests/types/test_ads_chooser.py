
from simulmedia.types.ad_chooser import AdChooser


class TestAdChooser:
    def test__lookup__not_found(self):
        assert AdChooser.lookup('ThisIsATotallyBogusValue') is None

    def test__lookup__happy_path(self):
        for e in AdChooser:
            assert e.value == AdChooser.lookup(e.value).value
