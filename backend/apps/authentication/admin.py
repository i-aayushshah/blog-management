from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin interface for User model.
    """
    list_display = [
        'email', 'username', 'get_full_name_display', 'is_email_verified',
        'is_active', 'is_staff', 'date_joined', 'last_login'
    ]
    list_filter = [
        'is_email_verified', 'is_active', 'is_staff', 'is_superuser',
        'date_joined', 'last_login'
    ]
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']
    readonly_fields = ['date_joined', 'last_login', 'created_at', 'updated_at']

    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'phone_number', 'profile_picture')
        }),
        ('Email Verification', {
            'fields': ('is_email_verified', 'email_verification_token', 'email_verification_expires'),
            'classes': ('collapse',)
        }),
        ('Password Reset', {
            'fields': ('password_reset_token', 'password_reset_expires'),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('date_joined', 'last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    def get_full_name_display(self, obj):
        """Display full name with verification status."""
        full_name = obj.get_full_name()
        if obj.is_email_verified:
            return format_html(
                '<span style="color: green;">✓ {}</span>',
                full_name
            )
        else:
            return format_html(
                '<span style="color: red;">✗ {}</span>',
                full_name
            )
    get_full_name_display.short_description = 'Full Name'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related()

    actions = ['verify_selected_users', 'unverify_selected_users']

    def verify_selected_users(self, request, queryset):
        """Mark selected users as verified."""
        updated = queryset.update(is_email_verified=True)
        self.message_user(
            request,
            f'Successfully verified {updated} user(s).'
        )
    verify_selected_users.short_description = "Mark selected users as verified"

    def unverify_selected_users(self, request, queryset):
        """Mark selected users as unverified."""
        updated = queryset.update(is_email_verified=False)
        self.message_user(
            request,
            f'Successfully unverified {updated} user(s).'
        )
    unverify_selected_users.short_description = "Mark selected users as unverified"
