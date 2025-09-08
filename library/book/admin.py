from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_authors', 'count', 'is_available', 'get_description_short')
    list_filter = ('count',)
    search_fields = ('name', 'description', 'id')
    ordering = ('name',)
    filter_horizontal = ('authors',)
    list_editable = ('count',)


    fieldsets = (
        ('Book Information', {
            'fields': ('name', 'description', 'authors'),
            'classes': ('wide',),
            'description': 'Book information constantly'
        }),
        ('Exist (valuable)', {
            'fields': ('count',),
            'classes': ('wide',),
            'description': 'Change information if it exists'
        }),
        ('System Information', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('id',)
    ordering = ('-id',)


    def get_authors(self, obj):
        authors = obj.authors.all()
        if authors:
            return ", ".join([f"{author.name} {author.surname}" for author in authors])
        return "None authors"

    get_authors.short_description = 'Authors'
    get_authors.admin_order_field = 'authors'


    def is_available(self, obj):
        return obj.count > 0

    is_available.boolean = True
    is_available.short_description = 'Available'

    def get_description_short(self, obj):
        if obj.description:
            return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
        return "None description"
    get_description_short.short_description = 'Description short'

    actions = ['make_unavailable', 'add_copies', 'reset_count']

    def make_unavailable(self, request, queryset):
        updated = queryset.update(count=0)
        self.message_user(request, f'{updated} books unavailable')
    make_unavailable.short_description = 'Make unavailable (count = 0)'

    def add_copies(self, request, queryset):
        updated = 0
        for book in queryset:
            book.count += 1
            book.save()
            updated += 1
        self.message_user(request, f'Added 1 copy for {updated} book.')
    add_copies.short_description = 'Add copies'

    def reset_count(self, request, queryset):
        updated = queryset.update(count=10)
        self.message_user(request, f'Count of 10 for {updated} books.')
    reset_count.short_description = 'Make count 10'

    list_per_page = 25
    list_max_show_all = 100
    save_on_top = True