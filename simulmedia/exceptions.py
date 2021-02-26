
class InvalidInputException(Exception):
    def __init__(self, message: str):
        super(InvalidInputException, self).__init__(message)


class InvalidAdConfigException(InvalidInputException):
    def __init__(self, message: str):
        super(InvalidAdConfigException, self).__init__(message)


class InvalidLanguageException(InvalidInputException):
    def __init__(self, message: str):
        super(InvalidLanguageException, self).__init__(message)


class InvalidCountryException(InvalidInputException):
    def __init__(self, message: str):
        super(InvalidCountryException, self).__init__(message)
