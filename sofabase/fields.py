from datetime import datetime
from hashlib import sha256

from .exceptions import ValidateError


class BaseField(object):

    __value__ = None
    
    def __init__(self, is_key=False, *args, **kwargs):
        self.is_key = is_key

    def __str__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.value)

    def __repr__(self):
        return self.__str__()

    @property
    def value(self):
        return self.__value__

    @value.setter
    def value(self, _value):
        self.__value__ = _value

    def validate(self):
        return True


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
    def value(self, _value):
        if isinstance(_value, str):
            _value = _value.encode('utf-8')
        self.__value__ = sha256(_value).hexdigest()


class DateTimeField(BaseField):

    def validate(self):
        if not isinstance(self.value, datetime):
            raise ValidateError('value shoulde be datetime type.')
        super(DateTimeField, self).validate()
