class BaseError(Exception):
    pass


class ValidateError(BaseError):
    pass


class KeyExistsError(BaseError):
    pass

class NotExistsError(BaseError):
    pass

