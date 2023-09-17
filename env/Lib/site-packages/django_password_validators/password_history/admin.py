from django.contrib import admin

from .models import PasswordHistory, UserPasswordHistoryConfig


class UserPasswordHistoryConfigAdmin(admin.ModelAdmin):

    list_display = ('user', 'date', 'iterations')
    list_filter = ('date', )
    ordering = ('date', )


class PasswordHistoryAdmin(admin.ModelAdmin):

    list_display = ('user_config', 'date', )
    list_filter = ('date', )
    ordering = ('date', )

admin.site.register(UserPasswordHistoryConfig, UserPasswordHistoryConfigAdmin)
admin.site.register(PasswordHistory, PasswordHistoryAdmin)
