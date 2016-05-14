from couchbase.bucket import Bucket
from couchbase.exceptions import KeyExistsError as KeyExistsError_

from .exceptions import KeyExistsError
from .fields import BaseField


class Model(object):

    __bucket__ = ''
    __primary_key_field__ = ''
    __fields__ = {}
    
    def __init__(self, *args, **kwargs):
        self.setup_fields(kwargs)

    def get_document(self):
        document = {}
        for name, field in self.__fields__.items():
            field.validate()
            if field.is_key:
                continue
            document[name] = field.get_string()
        return document

    def setup_fields(self, fields):
        field_names = fields.keys()

        for name in dir(self):
            attr = getattr(self, name)
            if isinstance(attr, BaseField):
                if name != 'primary_key' and attr.is_key:
                    self.__primary_key_field__ = name
                if name in field_names:
                    attr.value = fields[name]
                self.__fields__[name] = attr

    @property
    def primary_key(self):
        return getattr(self, self.__primary_key_field__, '')


class SofaBase(object):

    buckets = {}

    def __init__(self, base_host):
        self.base_host = base_host if base_host.endswith('/') else ''.join((base_host, '/'))
    
    def add(self, model):
        bucket = self.get_bucket(model.__bucket__)
        document = model.get_document()
        try:
            bucket.insert(model.primary_key.value, document)
        except KeyExistsError_:
            raise KeyExistsError

    def delete(self, model):
        bucket = self.get_bucket(model.__bucket__)
        bucket.delete(model.primary_key.value)

    def get(self, model):
        bucket = self.get_bucket(model.__bucket__)
        for key, value in bucket.get(model.primary_key.value).value.items():
            getattr(model, key).value = value
        return model
        
    def get_bucket(self, bucket_name):
        if bucket_name not in self.buckets:
            host = ''.join((self.base_host, bucket_name))
            self.buckets[bucket_name] = Bucket(host)
        return self.buckets[bucket_name]

    def set(self, model):
        bucket = self.get_bucket(model.__bucket__)
        document = model.get_document()
        bucket.set(model.primary_key.value, document)

