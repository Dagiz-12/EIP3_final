from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage, Subscriber
from django.utils.text import Truncator


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_date',
                    'status', 'message_preview')
    list_filter = ('status', 'created_date')
    list_editable = ('status',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_date', 'ip_address')
    date_hierarchy = 'created_date'

    fieldsets = (
        ('Message Details', {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Meta Information', {
            'fields': ('status', 'created_date', 'ip_address')
        }),
    )

    def message_preview(self, obj):
        preview = Truncator(obj.message).chars(50)
        return format_html('<span title="{}">{}</span>', obj.message, preview)
    message_preview.short_description = 'Message Preview'

    def has_add_permission(self, request):
        # Prevent adding contact messages manually through admin
        return False


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_date')
    list_filter = ('is_active', 'subscribed_date')
    list_editable = ('is_active',)
    search_fields = ('email',)
    readonly_fields = ('subscribed_date', 'token')
    date_hierarchy = 'subscribed_date'

    fieldsets = (
        ('Subscriber Information', {
            'fields': ('email', 'is_active')
        }),
        ('Meta Information', {
            'fields': ('subscribed_date', 'token')
        }),
    )
