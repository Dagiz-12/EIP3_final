from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContactView.as_view(), name='contact'),
    path('api/contact/', views.api_contact, name='contact_api'),
]
