from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog_list'),
    path('news/', views.PostListView.as_view(), name='news_list'),
    path('categories/', views.CategoryListView.as_view(), name='blog_categories'),
    path('tag/<slug:slug>/', views.PostListView.as_view(), name='posts_by_tag'),
    path('category/<slug:slug>/', views.PostListView.as_view(),
         name='posts_by_category'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='blog_detail'),
]
