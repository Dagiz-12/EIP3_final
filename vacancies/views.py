from core.utils.email import send_application_notification, send_application_confirmation
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
        from django.utils import timezone
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

        # Send email notifications
        try:
            # Send notification to admin
            send_application_notification(application)

            # Send confirmation to applicant
            send_application_confirmation(application)

        except Exception as e:
            # Log error but don't crash the form submission
            print(f"Email sending failed: {e}")

        messages.success(
            self.request,
            f'Thank you for applying for {vacancy.title}! We have sent a confirmation email and will review your application.'
        )

        return super().form_valid(form)
