from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Core app
    path('', include('core.urls')),

    # Blog/News app
    path('blog/', include('blog.urls')),
    path('news/', RedirectView.as_view(url='/blog/?type=news', permanent=True)),

    # Publications app
    path('publications/', include('publications.urls')),

    # Vacancies app
    path('vacancies/', include('vacancies.urls')),
    path('careers/', RedirectView.as_view(url='/vacancies/', permanent=True)),

    # Contacts app
    path('contact/', include('contacts.urls')),
    path('contact-us/', RedirectView.as_view(url='/contact/', permanent=True)),

    # CKEditor URL (for file uploads in admin)
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# Error handlers
handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'
handler403 = 'core.views.handler403'
handler400 = 'core.views.handler400'
