from django.contrib import admin
from django.utils.html import format_html
from .models import SliderImage, GuidingPrinciple, Partner, BoardMember, Strategy


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'image_preview')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'


@admin.register(GuidingPrinciple)
class GuidingPrincipleAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'icon')
    list_editable = ('order',)
    search_fields = ('title', 'description')


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'is_active', 'logo_preview')
    list_filter = ('is_active',)
    search_fields = ('name', 'website')

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 30px; max-width: 100px;" />', obj.logo.url)
        return "No Logo"
    logo_preview.short_description = 'Logo'


@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order', 'photo_preview')
    list_editable = ('order',)
    search_fields = ('name', 'position')

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 50%;" />', obj.photo.url)
        return "No Photo"
    photo_preview.short_description = 'Photo'


@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'icon')
    list_editable = ('order',)
    search_fields = ('title', 'description')
