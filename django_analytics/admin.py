from django.contrib import admin
from .models import PageView, Visitor, UserAgent


@admin.register(UserAgent)
class UserAgentAdmin(admin.ModelAdmin):
    readonly_fields = (
        "browser",
        "browser_version",
        "device_type",
        "device_brand",
        "device_family",
        "device_model",
        "os_family",
        "os_version",
        "touch_screen",
    )


class VisitorAdmin(admin.StackedInline):
    readonly_fields = ("created", "user", "session", "ip", "user_agent", "view")
    model = Visitor
    can_delete = False
    show_change_link = True
    extra = 0


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):

    inlines = [
        VisitorAdmin,
    ]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(
            set(
                [field.name for field in self.opts.local_fields]
                + [field.name for field in self.opts.local_many_to_many]
            )
        )

        if "is_submitted" in readonly_fields:
            readonly_fields.remove("is_submitted")

        return readonly_fields
