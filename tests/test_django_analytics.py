from importlib import import_module

from django.test import TestCase, override_settings
from django.conf import settings
from django.contrib.auth.models import User
from django_analytics.models import UserAgent, Visitor, PageView
from django.urls import reverse

from .models import Article


@override_settings(ROOT_URLCONF="tests.urls")
class DjangoAnalyticTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("test", "test@example.com", "test")
        self.article = Article.objects.create(
            name="First article", slug="first-article"
        )
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

    def test_middleware(self):
        self.client.force_login(user=self.user)

        url = reverse("article-detail", kwargs={"slug": self.article.slug})
        response = self.client.get(
            url,
            REMOTE_ADDR="127.0.0.1",
            HTTP_USER_AGENT="Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "article_detail.html")
        self.assertEqual(response.context["article"], self.article)
        self.assertEqual(UserAgent.objects.all().count(), 1)
        self.assertEqual(UserAgent.objects.first().browser, "Mobile Safari")
        self.assertEqual(Visitor.objects.get(user=self.user).user, self.user)
        self.assertTrue(Visitor.objects.get(user=self.user).session)
        self.assertTrue(PageView.objects.all())
        self.assertEqual(PageView.objects.first().view, 1)

        self.client.logout()
        session = self.client.session
        session["key"] = "value"
        session.save()

        response = self.client.get(
            url,
            REMOTE_ADDR="127.0.0.1",
            HTTP_USER_AGENT="Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["article"], self.article)
        self.assertEqual(UserAgent.objects.all().count(), 2)
        self.assertEqual(UserAgent.objects.get(id=2).browser, "Firefox")
        self.assertEqual(
            Visitor.objects.get(id=2).session,
            self.client.session.session_key,
        )
        self.assertTrue(PageView.objects.all())
        self.assertEqual(PageView.objects.first().view, 2)
        self.assertEqual(PageView.objects.first().object_id, self.article.id)
