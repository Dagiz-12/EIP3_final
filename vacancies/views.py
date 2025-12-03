from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Vacancy, Application
from .forms import ApplicationForm


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'vacancies/list.html'
    context_object_name = 'vacancies'
    paginate_by = 10

    def get_queryset(self):
        today = timezone.now().date()
        return Vacancy.objects.filter(
            is_published=True,
            deadline__gte=today
        ).order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Career Opportunities'
        context['active_vacancies'] = self.get_queryset().count()
        return context


class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = 'vacancies/detail.html'
    context_object_name = 'vacancy'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        today = timezone.now().date()
        return Vacancy.objects.filter(
            is_published=True,
            deadline__gte=today
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.title
        context['form'] = ApplicationForm()
        return context


class ApplicationCreateView(CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'vacancies/apply.html'

    def get_success_url(self):
        return reverse_lazy('vacancy_detail', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancy'] = get_object_or_404(
            Vacancy, slug=self.kwargs['slug'])
        return context

    def form_valid(self, form):
        vacancy = get_object_or_404(Vacancy, slug=self.kwargs['slug'])

        # Check if deadline hasn't passed
        if vacancy.deadline < timezone.now().date():
            messages.error(self.request, 'Application deadline has passed.')
            return self.form_invalid(form)

        # Set vacancy for the application
        application = form.save(commit=False)
        application.vacancy = vacancy

        # Get client IP address
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            application.ip_address = x_forwarded_for.split(',')[0]
        else:
            application.ip_address = self.request.META.get('REMOTE_ADDR')

        application.save()

        # Send email notification (optional)
        self.send_notification_email(application)

        messages.success(
            self.request,
            f'Thank you for applying for {vacancy.title}! We will review your application.'
        )

        return super().form_valid(form)

    def send_notification_email(self, application):
        """Send email notification to admin"""
        subject = f'New Application: {application.vacancy.title}'
        message = f'''
        New job application received:
        
        Position: {application.vacancy.title}
        Applicant: {application.full_name}
        Email: {application.email}
        Phone: {application.phone}
        Applied: {application.applied_date}
        
        You can view the application in the admin panel.
        '''

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],  # Add your admin email in settings
            fail_silently=True,
        )
