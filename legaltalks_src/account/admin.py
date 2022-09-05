from django.contrib import admin
from .models import (
    Account,
    ValidEnrollNo,
    UserProfile,
    CommonUserProfile
)
from django.contrib.auth.admin import UserAdmin

class AccountAdminConfig(UserAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'is_staff',
        'is_superuser'
    )
    search_fields = ('email', 'first_name', 'username')
    ordering = ('-email',)
    list_filter = ('is_moderator', 'is_advocate')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        ('Related Information', {'fields': ('is_moderator', 'is_advocate', 'enrollment_no')})
    )
    add_fieldsets = (
        (None,
        {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'password1', 'password2', 'is_advocate')
        }),
    )

admin.site.register(Account, AccountAdminConfig)
admin.site.register(ValidEnrollNo)
admin.site.register(UserProfile)
admin.site.register(CommonUserProfile)