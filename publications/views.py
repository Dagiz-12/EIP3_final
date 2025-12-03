from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Publication, PublicationCategory


class PublicationListView(ListView):
    model = Publication
    template_name = 'publications/list.html'
    context_object_name = 'publications'
    paginate_by = 12

    def get_queryset(self):
        queryset = Publication.objects.all().order_by('-published_date')

        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Search
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get categories for filter
        context['categories'] = PublicationCategory.objects.annotate(
            publication_count=Count('publication')
        ).order_by('name')

        # Get current category if any
        category_slug = self.request.GET.get('category')
        if category_slug:
            context['current_category'] = get_object_or_404(
                PublicationCategory, slug=category_slug)

        # Get search query
        context['search_query'] = self.request.GET.get('q', '')
        context['page_title'] = 'Publications'

        return context


class PublicationDetailView(DetailView):
    model = Publication
    template_name = 'publications/detail.html'
    context_object_name = 'publication'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        publication = self.object

        # Increment download count on view (or we could increment on actual download)
        # For now, we'll track views
        publication.download_count += 1
        publication.save(update_fields=['download_count'])

        # Get related publications
        related_publications = Publication.objects.filter(
            category=publication.category
        ).exclude(id=publication.id)[:4]

        context['related_publications'] = related_publications
        context['page_title'] = publication.title
        context['meta_description'] = publication.description[:160]

        return context


def download_publication(request, slug):
    """View to handle file downloads and track counts"""
    publication = get_object_or_404(Publication, slug=slug)

    # Increment download count
    publication.download_count += 1
    publication.save(update_fields=['download_count'])

    # Create download response
    from django.http import FileResponse
    response = FileResponse(publication.file.open(), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{publication.file.name}"'

    return response
