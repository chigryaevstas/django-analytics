from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F
from django.utils.translation import gettext_lazy as _

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")


class UserAgent(models.Model):
    """
    Model storing information about the user's device.
    None of the fields are editable because they are all dynamically created.
    """

    browser = models.CharField(max_length=40, blank=False, null=False, editable=False)
    browser_version = models.CharField(
        max_length=40, blank=False, null=False, editable=False
    )
    device_type = models.CharField(max_length=40, blank=True, null=True, editable=False)
    device_brand = models.CharField(
        max_length=40, blank=True, null=True, editable=False
    )
    device_family = models.CharField(
        max_length=40, blank=True, null=True, editable=False
    )
    device_model = models.CharField(max_length=40, db_index=True, editable=False)
    os_family = models.CharField(max_length=40, blank=True, null=True, editable=False)
    os_version = models.CharField(max_length=40, blank=True, null=True, editable=False)
    touch_screen = models.BooleanField(
        max_length=40, blank=True, null=True, editable=False
    )

    class Meta:
        verbose_name = _("User Agent")
        verbose_name_plural = _("User Agents")

    def __str__(self) -> str:
        return f"{self.browser}/{self.browser_version}"


class PageView(models.Model):
    """
    Model that stores the view totals for any content object.
    None of the fields are editable because they are all dynamically created.
    """

    view = models.PositiveIntegerField(default=0)
    modified = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="content_type_set_for_%(class)s",
    )
    object_id = models.PositiveIntegerField(verbose_name="object ID")
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ("-view",)
        get_latest_by = "modified"
        verbose_name = _("Page View")
        verbose_name_plural = _("Page Views")
        unique_together = ("content_type", "object_id")

    def __str__(self) -> str:
        return f"{self.content_object}"

    def increase(self):
        self.view = F("view") + 1
        self.save()


class Visitor(models.Model):
    """
    The main model that stores information about views.
    None of the fields are editable because they are all dynamically created.

    """

    created = models.DateTimeField(auto_now_add=True, db_index=True, editable=False)
    user = models.ForeignKey(
        AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, editable=False
    )
    ip = models.CharField(max_length=40, db_index=True, editable=False)
    session = models.CharField(max_length=40, editable=False)
    user_agent = models.ForeignKey(
        UserAgent, blank=True, null=True, on_delete=models.CASCADE, editable=False
    )
    view = models.ForeignKey(PageView, on_delete=models.CASCADE, editable=False)

    class Meta:
        ordering = ("-created",)
        get_latest_by = "created"
        verbose_name = _("Visitor")
        verbose_name_plural = _("Visitors")

    def __str__(self) -> str:
        return f"{self.user}"

    def save(self, *args, **kwargs):

        if self.pk is None:
            self.view.increase()

        super(Visitor, self).save(*args, **kwargs)
