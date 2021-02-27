

class DBException(Exception):
    def __init__(self, message: str):
        super(DBException, self).__init__(message)


# ================================================================================
# ConfigException
# ================================================================================
class ConfigException(Exception):
    def __init__(self, message: str):
        super(ConfigException, self).__init__(message)


class DBConfigException(ConfigException):
    def __init__(self, message: str):
        super(DBConfigException, self).__init__(message)


# ================================================================================
# InvalidInputException
# ================================================================================
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


class InvalidUserException(InvalidInputException):
    def __init__(self, message: str):
        super(InvalidUserException, self).__init__(message)


# ================================================================================
# ExternalServiceException
# ================================================================================
class ExternalServiceException(Exception):
    def __init__(self, message: str):
        super(ExternalServiceException, self).__init__(message)


class AdSourceServiceException(ExternalServiceException):
    def __init__(self, message: str):
        super(AdSourceServiceException, self).__init__(message)

