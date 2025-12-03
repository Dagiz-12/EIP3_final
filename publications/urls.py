from django.urls import path
from . import views

urlpatterns = [
    path('', views.PublicationListView.as_view(), name='publications_list'),
    path('<slug:slug>/', views.PublicationDetailView.as_view(),
         name='publication_detail'),
    path('<slug:slug>/download/', views.download_publication,
         name='download_publication'),
]
