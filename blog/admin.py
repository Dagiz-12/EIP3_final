from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import Truncator
from .models import Post, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = 'Posts'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = 'Posts'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_type', 'author',
                    'published_date', 'is_published', 'views', 'image_preview')
    list_filter = ('post_type', 'is_published', 'categories', 'published_date')
    list_editable = ('is_published',)
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories', 'tags')
    readonly_fields = ('views', 'published_date', 'updated_date')
    date_hierarchy = 'published_date'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'post_type', 'featured_image')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Meta Information', {
            'fields': ('author', 'categories', 'tags')
        }),
        ('Publication', {
            'fields': ('is_published', 'published_date', 'updated_date')
        }),
        ('Statistics', {
            'fields': ('views',)
        }),
    )

    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px;" />', obj.featured_image.url)
        return "No Image"
    image_preview.short_description = 'Featured Image'

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
