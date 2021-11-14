from types import ModuleType, FunctionType
from django.contrib.contenttypes.models import ContentType
from .models import Visitor, PageView, UserAgent
from typing import Dict
import importlib
from .utils import Info
from django.http.request import HttpRequest


class Provider:
    """

    A class that provides the ability to dynamically import models from View classes.
    As well as the ability to extract data about users and save it to the database.

    """

    def __init__(
        self, request: HttpRequest, view_func: FunctionType, view_kwargs: Dict
    ) -> None:
        self._slug = view_kwargs
        self.request = request
        self._model = view_func

    def _dynamic_import(self) -> ModuleType:
        """

        Retrieves a database from the class-view.

        **NOTE** The view must use class-based views. In which the model should be indicated.
            https://docs.djangoproject.com/en/3.2/topics/class-based-views/
        """
        import_module = importlib.import_module(self._model.__module__)
        self.import_view_cls = getattr(import_module, self._model.__name__)

    def add(self) -> None:

        """

        Invokes a dynamic import of the database.
        Retrieves data from the request function and stores it in the database.

        """

        self._dynamic_import()

        # Retrieving a model from view.
        db = self.import_view_cls.model

        # Getting the ID of the post that is being viewed.
        view_entry = db.objects.get(**self._slug)

        # Getting the ID of the model to save the content type.
        content_type = ContentType.objects.get_for_model(view_entry)

        # We check if this post has been viewed before or create the first view.
        try:
            view = PageView.objects.get(
                content_type__pk=content_type.pk, object_id=view_entry.pk
            )
        except PageView.DoesNotExist:
            view = PageView.objects.create(content_object=view_entry)

        # Preparing data about user.
        user = self.request.user
        info = Info(self.request)
        ip = info.get_ip
        session_key = self.request.session.session_key
        user_agent = UserAgent(**info.get_user_agent)

        visiter = Visitor(
            ip=ip,
            user_agent=user_agent,
            session=session_key,
            view=view,
        )

        # If users are logged in. Stored data about visits for the logged in user.
        # Otherwise, we save by the session ID
        if self.request.user.is_authenticated:
            if not Visitor.objects.filter(user=user, view=view):
                visiter.user = user
                user_agent.save()
                visiter.save()
        else:
            if not Visitor.objects.filter(session=session_key, view=view):
                user_agent.save()
                visiter.save()
