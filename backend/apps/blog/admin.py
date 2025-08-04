from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Category model.
    """
    list_display = ['name', 'slug', 'post_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def post_count(self, obj):
        """Display post count with link."""
        count = obj.post_count
        return format_html(
            '<a href="?category__id__exact={}">{}</a>',
            obj.id, count
        )
    post_count.short_description = 'Posts'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin interface for Tag model.
    """
    list_display = ['name', 'slug', 'post_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {
            'fields': ('name', 'slug')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def post_count(self, obj):
        """Display post count with link."""
        count = obj.post_count
        return format_html(
            '<a href="?tags__id__exact={}">{}</a>',
            obj.id, count
        )
    post_count.short_description = 'Posts'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin interface for Post model.
    """
    list_display = [
        'title', 'author', 'category', 'status', 'is_published_display',
        'reading_time', 'created_at', 'published_at'
    ]
    list_filter = [
        'status', 'category', 'tags', 'author', 'created_at', 'published_at'
    ]
    search_fields = ['title', 'content', 'excerpt', 'author__email', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'published_at', 'reading_time_display']
    filter_horizontal = ['tags']

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt')
        }),
        ('Relationships', {
            'fields': ('author', 'category', 'tags')
        }),
        ('Status & Media', {
            'fields': ('status', 'featured_image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('reading_time_display',),
            'classes': ('collapse',)
        }),
    )

    def is_published_display(self, obj):
        """Display published status with color."""
        if obj.is_published:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Published</span>'
            )
        else:
            return format_html(
                '<span style="color: orange; font-weight: bold;">✗ Draft</span>'
            )
    is_published_display.short_description = 'Status'

    def reading_time_display(self, obj):
        """Display reading time in admin."""
        return f"{obj.reading_time} minute{'s' if obj.reading_time != 1 else ''}"
    reading_time_display.short_description = 'Reading Time'

    def get_queryset(self, request):
        """Optimize queryset with select_related and prefetch_related."""
        return super().get_queryset(request).select_related(
            'author', 'category'
        ).prefetch_related('tags')

    actions = ['publish_selected_posts', 'unpublish_selected_posts']

    def publish_selected_posts(self, request, queryset):
        """Publish selected posts."""
        from django.utils import timezone
        updated = queryset.update(
            status='published',
            published_at=timezone.now()
        )
        self.message_user(
            request,
            f'Successfully published {updated} post(s).'
        )
    publish_selected_posts.short_description = "Publish selected posts"

    def unpublish_selected_posts(self, request, queryset):
        """Unpublish selected posts."""
        updated = queryset.update(
            status='draft',
            published_at=None
        )
        self.message_user(
            request,
            f'Successfully unpublished {updated} post(s).'
        )
    unpublish_selected_posts.short_description = "Unpublish selected posts"

    def save_model(self, request, obj, form, change):
        """Auto-set author if not set."""
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
