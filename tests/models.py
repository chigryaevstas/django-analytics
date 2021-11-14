from django.db import models
from django.urls import reverse


class Article(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("article:article-detail", kwargs={"slug": self.slug})
