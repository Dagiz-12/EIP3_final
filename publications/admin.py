from django.contrib import admin
from django.utils.html import format_html
from .models import Publication, PublicationCategory


@admin.register(PublicationCategory)
class PublicationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'publication_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def publication_count(self, obj):
        return obj.publication_set.count()
    publication_count.short_description = 'Publications'


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_date',
                    'download_count', 'is_featured', 'cover_preview')
    list_filter = ('category', 'is_featured', 'published_date')
    list_editable = ('is_featured',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('download_count', 'published_date')
    date_hierarchy = 'published_date'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'description')
        }),
        ('Files', {
            'fields': ('cover_image', 'file')
        }),
        ('Publication', {
            'fields': ('is_featured', 'published_date')
        }),
        ('Statistics', {
            'fields': ('download_count',)
        }),
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 35px;" />', obj.cover_image.url)
        return "No Cover"
    cover_preview.short_description = 'Cover'
