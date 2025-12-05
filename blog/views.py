from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q, F, Count  # ← IMPORT Count HERE
from django.utils import timezone
from .models import Post, Category, Tag, PostView
from django.utils.html import strip_tags
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class PostListView(ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        queryset = Post.objects.filter(status='published')

        # Filter by post type
        post_type = self.request.GET.get('type', '')
        if post_type in ['news', 'blog', 'implementation']:
            queryset = queryset.filter(post_type=post_type)

        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)

        # Search
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(excerpt__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()

        return queryset.order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_type = self.request.GET.get('type', '')
        context['post_type'] = post_type
        context['search_query'] = self.request.GET.get('q', '')

        # Get categories with post counts - FIXED IMPORT
        categories = Category.objects.annotate(
            post_count=Count(
                'post',
                filter=Q(post__status='published') &
                (Q(post__post_type=post_type) if post_type else Q())
            )
        ).filter(post_count__gt=0, is_active=True).order_by('order')

        context['categories'] = categories

        # Recent posts for sidebar (exclude current posts)
        current_post_ids = [post.id for post in context['posts']]
        context['recent_posts'] = Post.objects.filter(
            status='published'
        ).exclude(
            id__in=current_post_ids
        ).order_by('-published_date')[:5]

        # Popular tags
        context['tags'] = Tag.objects.annotate(
            post_count=Count('post', filter=Q(post__status='published'))
        ).filter(post_count__gt=0).order_by('-post_count')[:10]

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        # Only show published posts or drafts for staff
        queryset = Post.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(status='published') &
                Q(published_date__lte=timezone.now())
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Increment views
        if self.object.status == 'published':
            self.object.increment_views()

            # Track view with IP
            PostView.objects.create(
                post=self.object,
                ip_address=self.get_client_ip(),
                user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
                referer=self.request.META.get('HTTP_REFERER', '')
            )

        # Related posts (same category, published status)
        context['related_posts'] = Post.objects.filter(
            status='published',
            categories__in=self.object.categories.all()
        ).exclude(
            id=self.object.id
        ).distinct().order_by('-published_date')[:3]

        return context

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
        return context


class PostsByCategoryView(ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        return Post.objects.filter(
            status='published',
            categories=self.category
        ).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostsByTagView(ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(
            status='published',
            tags=self.tag
        ).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
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
