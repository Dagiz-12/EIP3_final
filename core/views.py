from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from .models import SliderImage, GuidingPrinciple, Partner, BoardMember, Strategy
from blog.models import Post, Category
from publications.models import Publication
from vacancies.models import Vacancy
from contacts.models import Subscriber
from contacts.forms import SubscriptionForm

from django.http import Http404


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get cached data or compute
        cache_key = 'home_page_data'
        data = cache.get(cache_key)

        if not data:
            data = {
                'slider_images': SliderImage.objects.filter(is_active=True).order_by('order'),
                'recent_news': Post.objects.filter(
                    post_type='news',
                    is_published=True
                )[:6],
                'guiding_principles': GuidingPrinciple.objects.all()[:6],
                'partners': Partner.objects.filter(is_active=True),
                'featured_publications': Publication.objects.filter(
                    is_featured=True
                )[:4],
            }
            cache.set(cache_key, data, 60 * 15)  # Cache for 15 minutes

        context.update(data)
        return context


class WhoWeAreView(TemplateView):
    template_name = 'core/about/who_we_are.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Who We Are'
        context['page_description'] = 'Learn about EIP Ethiopia\'s history, mission, and vision'
        return context


class GuidingPrinciplesView(TemplateView):
    template_name = 'core/about/guiding_principles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        principles = GuidingPrinciple.objects.all().order_by('order')
        context['principles'] = principles
        context['page_title'] = 'Our Guiding Principles'
        return context


class StrategiesView(TemplateView):
    template_name = 'core/about/strategies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        strategies = Strategy.objects.all().order_by('order')
        context['strategies'] = strategies
        context['page_title'] = 'Strategies & Priorities'
        return context


class BoardMembersView(ListView):
    model = BoardMember
    template_name = 'core/about/board_members.html'
    context_object_name = 'members'
    ordering = ['order']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Board Members'
        return context


class WhatWeDoView(TemplateView):
    template_name = 'core/what_we_do.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # In a real implementation, you would have a Project model
        # For now, we'll use static data or blog posts with project category
        projects = Post.objects.filter(
            categories__name__icontains='project',
            is_published=True
        )[:6]
        context['projects'] = projects
        context['page_title'] = 'What We Do'
        return context


@csrf_exempt
@require_POST
def subscribe_newsletter(request):
    """API endpoint for newsletter subscription"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()

        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)

        # Simple email validation
        if '@' not in email or '.' not in email.split('@')[-1]:
            return JsonResponse({'error': 'Please enter a valid email address'}, status=400)

        # Check if already subscribed
        if Subscriber.objects.filter(email=email).exists():
            return JsonResponse({'message': 'You are already subscribed!'})

        # Create subscriber with unique token for unsubscribe
        subscriber = Subscriber.objects.create(
            email=email,
            token=str(uuid.uuid4())
        )

        # TODO: Send confirmation email
        # send_confirmation_email(subscriber)

        return JsonResponse({
            'message': 'Thank you for subscribing to our newsletter!',
            'status': 'success'
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)

# Custom error handlers


def handler404(request, exception):
    """Custom 404 error handler"""
    context = {
        'page_title': 'Page Not Found',
        'error_code': '404',
        'error_message': 'The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.'
    }
    return render(request, 'core/errors/404.html', context, status=404)


def handler500(request):
    """Custom 500 error handler"""
    context = {
        'page_title': 'Server Error',
        'error_code': '500',
        'error_message': 'An internal server error has occurred. Please try again later.'
    }
    return render(request, 'core/errors/500.html', context, status=500)


def handler403(request, exception):
    """Custom 403 error handler"""
    context = {
        'page_title': 'Permission Denied',
        'error_code': '403',
        'error_message': 'You do not have permission to access this page.'
    }
    return render(request, 'core/errors/403.html', context, status=403)


def handler400(request, exception):
    """Custom 400 error handler"""
    context = {
        'page_title': 'Bad Request',
        'error_code': '400',
        'error_message': 'The server cannot process the request due to a client error.'
    }
    return render(request, 'core/errors/400.html', context, status=400)
