from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Post, PostImage, PostView


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    fields = ['image', 'caption', 'alt_text', 'order']
    readonly_fields = ['created_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'order', 'post_count', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'post_type_display',
        'status_display',
        'author',
        'published_date',
        'views',
        'is_featured',
        'is_published'
    ]
    list_filter = ['post_type', 'status',
                   'categories', 'is_featured', 'published_date']
    search_fields = ['title', 'excerpt', 'content']
    readonly_fields = ['views', 'created_date',
                       'updated_date', 'reading_time_display']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'post_type', 'status')
        }),
        ('Images', {
            'fields': ('featured_image', 'featured_image_alt', 'og_image')
        }),
        ('Categories & Tags', {
            'fields': ('categories', 'tags')
        }),
        ('Dates', {
            'fields': ('published_date', 'created_date', 'updated_date')
        }),
        ('Featured & SEO', {
            'fields': ('is_featured', 'meta_description', 'meta_keywords', 'og_title', 'og_description')
        }),
        ('Statistics', {
            'fields': ('views', 'reading_time_display')
        }),
    )

    inlines = [PostImageInline]

    def post_type_display(self, obj):
        type_icons = {
            'news': '📰',
            'blog': '📝',
            'implementation': '🚀'
        }
        return f"{type_icons.get(obj.post_type, '')} {obj.get_post_type_display()}"
    post_type_display.short_description = 'Type'

    def status_display(self, obj):
        status_colors = {
            'draft': 'gray',
            'published': 'green',
            'archived': 'orange'
        }
        color = status_colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'

    def reading_time_display(self, obj):
        return f"{obj.reading_time} min"
    reading_time_display.short_description = 'Reading Time'


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'image_preview', 'caption', 'order']
    list_editable = ['order']
    search_fields = ['post__title', 'caption']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = 'Preview'


@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ['post', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at', 'post']
    search_fields = ['post__title', 'ip_address']
    readonly_fields = ['viewed_at']
