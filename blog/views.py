from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Post, Category, Tag


class PostListView(ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        queryset = Post.objects.filter(
            is_published=True).select_related('author')

        # Filter by post type (news or blog)
        post_type = self.request.GET.get('type', 'blog')
        if post_type in ['news', 'blog']:
            queryset = queryset.filter(post_type=post_type)

        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)

        # Filter by tag
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        # Search
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(excerpt__icontains=search_query) |
                Q(categories__name__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()

        return queryset.order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get filter parameters
        post_type = self.request.GET.get('type', 'blog')
        context['post_type'] = post_type
        context['page_title'] = 'News' if post_type == 'news' else 'Blog'

        # Get categories and tags for sidebar
        context['categories'] = Category.objects.annotate(
            post_count=Count('post')
        ).order_by('name')

        context['recent_posts'] = Post.objects.filter(
            is_published=True
        ).exclude(id__in=[p.id for p in context['posts']])[:5]

        # Get all tags
        context['tags'] = Tag.objects.annotate(
            post_count=Count('post')
        ).order_by('-post_count')[:10]

        # Get search query
        context['search_query'] = self.request.GET.get('q', '')

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # Increment view count
        post.views += 1
        post.save(update_fields=['views'])

        # Get related posts (same category)
        related_posts = Post.objects.filter(
            categories__in=post.categories.all(),
            is_published=True
        ).exclude(id=post.id).distinct()[:3]

        context['related_posts'] = related_posts
        context['page_title'] = post.title
        context['meta_description'] = post.excerpt
        context['meta_keywords'] = ', '.join(
            [tag.name for tag in post.tags.all()])

        return context


@method_decorator(cache_page(60 * 60), name='dispatch')  # Cache for 1 hour
class CategoryListView(ListView):
    model = Category
    template_name = 'blog/categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.annotate(
            post_count=Count('post')
        ).order_by('name')
