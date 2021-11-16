Django Analytics 
========================
The Django module that allows you to track views on a site. Works only with views based on `Django Class-based <https://docs.djangoproject.com/en/3.2/topics/class-based-views/>`_ views.

Installation
------------
1. Install with **pip**:

    .. code-block:: sh

        pip install git+https://github.com/chigryaevstas/django-analytics.git




2. Add 'django_analytics' to your ``INSTALLED_APPS`` setting:

    .. code-block:: python

        settings.py

        INSTALLED_APPS = [
            # ...,
            'django_analytics',
            # ...,
        ]

3. Add the middleware:

    .. code-block:: python

        MIDDLEWARE = [
            # ...,
            "django_analytics.middleware.Analytics",
            # ...,
        ]


Usage
-----
In order for `django_analytics` to start tracking, you need to mark the class view with the word `Tracking`.

.. code-block:: python

    from django.views.generic import DetailView
    from .models import Article


    class ArticleViewTracking(DetailView):
        model = Article
        ...
    ]


Changelog
---------

**Version 0.1.0**

* Initial release
