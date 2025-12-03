from django.urls import path
from . import views

urlpatterns = [
    path('', views.VacancyListView.as_view(), name='vacancies_list'),
    path('<slug:slug>/', views.VacancyDetailView.as_view(), name='vacancy_detail'),
    path('<slug:slug>/apply/', views.ApplicationCreateView.as_view(),
         name='apply_vacancy'),
]
