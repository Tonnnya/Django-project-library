from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ROLE_CHOICES

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    list_display = ('id','email', 'first_name', 'last_name', 'middle_name',
                    'get_role_display', 'is_active', 'created_at')

    list_filter = ('role', 'is_active', 'created_at')

    search_fields = ('email', 'first_name', 'last_name')

    ordering = ('-created_at',)
    list_editable = ('is_active',)

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
    ('Main information', {'fields': ('email', 'password')}),
    ('Personal info', {'fields': ('first_name', 'last_name', 'middle_name'),
                       'classes': ('wide',)}),
    ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser',)}),
    ('Groups', {'fields': ('groups', 'user_permissions')}),
    ('Dates', {'fields': ('created_at', 'updated_at')}),
    )

    add_fieldsets = (
    ('Create of user', {'fields': ('email', 'first_name', 'last_name', 'middle_name', 'password1', 'password2', 'role', 'is_active')}),
    ('Options', {'fields': ('is_staff', 'is_superuser',)}),
    )

    actions = ['activate_user', 'deactivate_user', 'make_librarian', 'make_visitor']

    def get_role_display(self, obj):
        return obj.get_role_name()
    get_role_display.short_description = 'Role'
    get_role_display.admin_order_field = 'role'

    def activate_user(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users have been activated.')
    activate_user.short_description = 'Activate users'

    def deactivate_user(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users have been deactivated.')
    deactivate_user.short_description = 'Deactivate users'

    def make_librarian(self, request, queryset):
        updated = queryset.update(role=1, is_staff=True)
        self.message_user(request, f'{updated} users have been marked as librarian.')
    make_librarian.short_description = 'Make librarians'

    def make_visitor(self, request, queryset):
        updated = queryset.update(role=0, is_staff=False, is_superuser=False)
        self.message_user(request, f'{updated} users have been marked as visitor.')
    make_visitor.short_description = 'Make visitors'

admin.site.site_header = 'Library System'
admin.site.site_title = 'Library Admin'
admin.site.site_title = 'Admin panel'

admin.site.site_url = '/home'

