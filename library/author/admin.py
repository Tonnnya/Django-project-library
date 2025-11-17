from django.contrib import admin
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname', 'name', 'patronymic', 'get_books_count')
    list_filter = ('surname',)
    search_fields = ('name', 'surname', 'patronymic', 'id')
    ordering = ('surname', 'name')

    fieldsets = (
        ('Author Information', {
            'fields': ('name', 'surname', 'patronymic'),
            'classes': ('wide',),
            'description': 'Author personal information'
        }),
        ('System Information', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('id',)

    def get_books_count(self, obj):
        """Display number of books by this author"""
        count = obj.books.count()
        return count if count > 0 else "No books"

    get_books_count.short_description = 'Books Count'

    list_per_page = 25
    list_max_show_all = 100
    save_on_top = True
