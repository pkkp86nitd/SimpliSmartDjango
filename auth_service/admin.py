from django.contrib import admin
from .models import User, Organization

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'get_organization_name', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'organization')

    def get_organization_name(self, obj):
        return obj.organization.name if obj.organization else None

    get_organization_name.admin_order_field = 'organization'  # Allows sorting by organization name
    get_organization_name.short_description = 'Organization'  # Display name in the admin panel

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'invite_code')
    search_fields = ('name', 'invite_code')

admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
