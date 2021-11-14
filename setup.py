# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_analytics']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.9,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'ua-parser>=0.10.0,<0.11.0',
 'user-agents>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'django-analytics',
    'version': '0.1.0',
    'description': '',
    'long_description': 'Django Analytics \n========================\nThe Django module that allows you to track views on a site. Works only with views based on Django [Class-based](https://docs.djangoproject.com/en/3.2/topics/class-based-views/) views.\n\nInstallation\n------------\n1. Install with **pip**:\n\n    .. code-block:: sh\n        pip install https://github.com/chigryaevstas/django-analytics/master.zip\n\n\n\n\n2. Add \'django_analytics\' to your ``INSTALLED_APPS`` setting:\n\n    .. code-block:: python\n        settings.py\n\n        INSTALLED_APPS = [\n            # ...,\n            \'django_analytics\',\n            # ...,\n        ]\n\n3. Add the middleware:\n\n    .. code-block:: python\n\n        MIDDLEWARE = [\n            # ...,\n            "django_analytics.middleware.Analytics",\n            # ...,\n        ]\n\n\nUsage\n-----\nIn order for `django_analytics` to start tracking, you need to mark the class view with the word `Tracking`.\n\n.. code-block:: python\n\n    from django.views.generic import DetailView\n    from .models import Article\n\n\n    class ArticleViewTracking(DetailView):\n        model = Article\n        ...\n    ]\n\n\nChangelog\n---------\n\n### Version 0.1.0\n\n* Initial release',
    'author': 'Chigryaev Stas',
    'author_email': 'chigryaevstas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chigryaevstas/django-analytics',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
