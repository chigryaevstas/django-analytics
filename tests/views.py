from django.views.generic import DetailView
from .models import Article


class ArticleViewTracking(DetailView):
    model = Article
    pk_url_kwargs = "slug"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "article"
    template_name = "article_detail.html"
