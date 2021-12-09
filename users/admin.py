from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_filter = ('role', )


admin.site.register(User, UserAdmin)
