from django.urls import path

from . import views

app_name = "article"

urlpatterns = [
    path("article/<slug:slug>/", views.ArticleView__.as_view(), name="article-detail"),
]
