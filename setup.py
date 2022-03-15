# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['progress_passthrough']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'progress-passthrough',
    'version': '0.1.0',
    'description': 'Utilities to pass progress information through nesting levels',
    'long_description': None,
    'author': 'smheidrich',
    'author_email': 'smheidrich@weltenfunktion.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
