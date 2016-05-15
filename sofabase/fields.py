from datetime import datetime
from hashlib import sha256

from .exceptions import ValidateError


class BaseField(object):

    __value__ = None
    
    def __init__(self, default=None, is_key=False, *args, **kwargs):
        self.default = default
        self.is_key = is_key

    def __str__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.value)

    def __repr__(self):
        return self.__str__()

    @property
    def value(self):
        if not self.__value__ and self.default:
            return self.default() if hasattr(self.default, '__call__') else self.default
        return self.__value__

    @value.setter
    def value(self, value_):
        self.__value__ = value_

    def validate(self):
        return True

    def get_string(self):
        return self.value.__str__()


class TextField(BaseField):
    
    max_length = None

    def __init__(self, max_length=None, *args, **kwargs):
        super(TextField, self).__init__(*args, **kwargs)
        self.max_length = max_length

    def validate(self):
        if self.max_length and self.max_length < len(self.value):
            raise ValidateError('length should be under %s.' % self.max_length)
        super(TextField, self).validate()


class NumberField(BaseField):
    
    @property
    def value(self):
        return str(self.__value__)


class PasswordField(BaseField):

    @BaseField.value.setter
    def value(self, value_):
        if isinstance(value_, str):
            value_ = value_.encode('utf-8')
        self.__value__ = sha256(value_).hexdigest()


class DateTimeField(BaseField):

    def validate(self):
        if self.value and not isinstance(self.value, datetime):
            raise ValidateError('value should be datetime type.')
        super(DateTimeField, self).validate()


class JsonField(BaseField):

    def __init__(self, scheme, *args, **kwargs):
        self.is_key = False
        self.scheme = scheme

    def validate(self):
        for key, value in self.value.items():
            if isinstance(value, dict):
                pass
