from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from apps.customauth.models import APIClient

User = get_user_model()


class CustomUserAdmin(BaseUserAdmin):
    """Custom admin for CustomUser model."""

    model = User
    list_display = ('email', 'username', 'first_name', 'last_name',
                    'user_type', 'is_active', 'is_staff', 'date_joined', 'slug')
    list_filter = ('user_type', 'is_active', 'is_staff',
                   'is_superuser', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'updated_at')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'slug')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('User Type', {'fields': ('user_type',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {
         'fields': ('date_joined', 'updated_at', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


class APIClientAdmin(admin.ModelAdmin):
    """Admin for APIClient model."""

    list_display = ('name', 'client_type', 'is_active',
                    'rate_limit', 'created_at')
    list_filter = ('client_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'api_key', 'created_at', 'updated_at')

    fieldsets = (
        (None, {'fields': ('name', 'description', 'id')}),
        ('Configuration', {
         'fields': ('client_type', 'api_key', 'rate_limit')}),
        ('Status', {'fields': ('is_active',)}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )

    actions = ['regenerate_api_keys', 'deactivate_clients', 'activate_clients']

    def regenerate_api_keys(self, request, queryset):
        """Action to regenerate API keys."""
        for client in queryset:
            client.regenerate_api_key()
        self.message_user(request, f'{queryset.count()} API keys regenerated.')

    regenerate_api_keys.short_description = 'Regenerate selected API keys'

    def deactivate_clients(self, request, queryset):
        """Action to deactivate clients."""
        queryset.update(is_active=False)
        self.message_user(request, f'{queryset.count()} clients deactivated.')

    deactivate_clients.short_description = 'Deactivate selected clients'

    def activate_clients(self, request, queryset):
        """Action to activate clients."""
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} clients activated.')

    activate_clients.short_description = 'Activate selected clients'


admin.site.register(User, CustomUserAdmin)
admin.site.register(APIClient, APIClientAdmin)
