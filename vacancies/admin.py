from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Vacancy, Application


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'job_type', 'location', 'deadline',
                    'is_published', 'application_count', 'days_remaining')
    list_filter = ('job_type', 'is_published', 'created_date')
    list_editable = ('is_published',)
    search_fields = ('title', 'description',
                     'requirements', 'responsibilities')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_date',)
    date_hierarchy = 'deadline'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'job_type', 'location')
        }),
        ('Details', {
            'fields': ('description', 'requirements', 'responsibilities')
        }),
        ('Publication', {
            'fields': ('deadline', 'is_published', 'created_date')
        }),
    )

    def application_count(self, obj):
        count = obj.application_set.count()
        url = reverse('admin:vacancies_application_changelist') + \
            f'?vacancy__id__exact={obj.id}'
        return format_html('<a href="{}">{}</a>', url, count)
    application_count.short_description = 'Applications'

    def days_remaining(self, obj):
        if obj.deadline:
            days = (obj.deadline - timezone.now().date()).days
            if days < 0:
                return format_html('<span style="color: red;">Expired</span>')
            elif days == 0:
                return format_html('<span style="color: orange;">Today</span>')
            elif days <= 7:
                return format_html('<span style="color: orange;">{} days</span>', days)
            else:
                return format_html('<span style="color: green;">{} days</span>', days)
        return 'N/A'
    days_remaining.short_description = 'Days Left'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'vacancy', 'email',
                    'applied_date', 'is_reviewed', 'resume_link')
    list_filter = ('is_reviewed', 'applied_date', 'vacancy')
    list_editable = ('is_reviewed',)
    search_fields = ('full_name', 'email', 'phone', 'cover_letter')
    readonly_fields = ('applied_date', 'ip_address')
    date_hierarchy = 'applied_date'

    fieldsets = (
        ('Application Information', {
            'fields': ('vacancy', 'full_name', 'email', 'phone')
        }),
        ('Documents', {
            'fields': ('cover_letter', 'resume', 'additional_documents')
        }),
        ('Status', {
            'fields': ('is_reviewed', 'applied_date', 'ip_address')
        }),
    )

    def resume_link(self, obj):
        if obj.resume:
            return format_html('<a href="{}" target="_blank">Download</a>', obj.resume.url)
        return "No Resume"
    resume_link.short_description = 'Resume'

    def has_add_permission(self, request):
        # Prevent adding applications manually through admin
        return False
