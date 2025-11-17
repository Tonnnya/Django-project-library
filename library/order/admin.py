from django.contrib import admin
from .models import Order
from django.utils.html import format_html


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_email', 'get_book_name', 'created_at', 'plated_end_at', 'end_at', 'get_status', 'get_overdue_status')
    list_filter = ('created_at', 'end_at', 'plated_end_at')
    search_fields = ('user__email', 'book__name', 'id')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'book'),
            'classes': ('wide',),
            'description': 'Order main information'
        }),
        ('Dates', {
            'fields': ('created_at', 'plated_end_at', 'end_at'),
            'classes': ('wide',),
            'description': 'Order dates'
        }),
        ('System Information', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('id', 'created_at')

    def get_user_email(self, obj):
        """Display user email"""
        return obj.user.email

    get_user_email.short_description = 'User'
    get_user_email.admin_order_field = 'user__email'

    def get_book_name(self, obj):
        """Display book name"""
        return obj.book.name

    get_book_name.short_description = 'Book'
    get_book_name.admin_order_field = 'book__name'

    def get_status(self, obj):
        """Display order status"""
        if obj.end_at:
            return format_html('<span style="color: green;">✓ Returned</span>')
        return format_html('<span style="color: orange;">⊙ Active</span>')

    get_status.short_description = 'Status'

    def get_overdue_status(self, obj):
        """Display if order is overdue"""
        if obj.end_at:
            return '-'
        if hasattr(obj, 'is_overdue') and obj.is_overdue:
            return format_html('<span style="color: red;">⚠ Overdue</span>')
        return format_html('<span style="color: green;">✓ On time</span>')

    get_overdue_status.short_description = 'Due Status'

    actions = ['mark_as_returned']

    def mark_as_returned(self, request, queryset):
        """Mark selected orders as returned"""
        from django.utils import timezone
        updated = 0
        for order in queryset.filter(end_at__isnull=True):
            order.end_at = timezone.now()
            order.save()
            # Increase book count
            order.book.count += 1
            order.book.save()
            updated += 1
        self.message_user(request, f'{updated} orders marked as returned')

    mark_as_returned.short_description = 'Mark as returned'

    list_per_page = 25
    list_max_show_all = 100
    save_on_top = True
