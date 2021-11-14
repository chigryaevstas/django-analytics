from django.urls import path

from .views import ArticleViewTracking

app_name = "article"

urlpatterns = [
    path("article/<slug:slug>/", ArticleViewTracking.as_view(), name="article-detail"),
]
