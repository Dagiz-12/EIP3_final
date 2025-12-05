from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/who-we-are/', views.WhoWeAreView.as_view(), name='about_who_we_are'),
    path('about/guiding-principles/', views.GuidingPrinciplesView.as_view(),
         name='about_guiding_principles'),
    path('about/strategies/', views.StrategiesView.as_view(),
         name='about_strategies'),
    path('about/board-members/', views.BoardMembersView.as_view(),
         name='about_board_members'),
    path('what-we-do/', views.WhatWeDoView.as_view(), name='what_we_do'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('api/subscribe/', views.subscribe_newsletter, name='subscribe_api'),

]
