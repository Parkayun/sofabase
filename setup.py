# -*- coding:utf-8 -*-
import re
from setuptools import setup


with open('sofabase/__init__.py') as f:
    version = re.search(r'__version__\s*=\s*\'(.+?)\'', f.read()).group(1)
assert version

setup(
    name="sofabase",
    version=version,
    packages=["sofabase"],
    install_requires=["couchbase>=2.0.8"],
    author="Ayun Park",
    author_email="iamparkayun@gmail.com",
    description="Couchbase Object Mapper",
    url="http://github.com/Parkayun/sofabase",
)

