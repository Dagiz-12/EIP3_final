from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ContactMessage, Subscriber
from .forms import ContactForm, SubscriptionForm


class ContactView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = 'contacts/contact.html'
    success_url = reverse_lazy('contact')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Contact Us'
        context['meta_description'] = 'Get in touch with EIP Ethiopia'
        return context

    def form_valid(self, form):
        # Get client IP address
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = self.request.META.get('REMOTE_ADDR')

        # Save with IP address
        contact_message = form.save(commit=False)
        contact_message.ip_address = ip_address
        contact_message.save()

        # Send email notification
        self.send_notification_email(contact_message)

        messages.success(
            self.request,
            'Thank you for your message! We will get back to you soon.'
        )

        return super().form_valid(form)

    def send_notification_email(self, contact_message):
        """Send email notification about new contact message"""
        subject = f'New Contact Message: {contact_message.subject}'
        message = f'''
        New contact form submission:
        
        Name: {contact_message.name}
        Email: {contact_message.email}
        Subject: {contact_message.subject}
        Message: {contact_message.message}
        
        IP Address: {contact_message.ip_address}
        Received: {contact_message.created_date}
        
        You can view and manage this message in the admin panel.
        '''

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],  # Add your admin email in settings
            fail_silently=True,
        )

        # Optional: Send auto-reply to user
        auto_reply_subject = 'Thank you for contacting EIP Ethiopia'
        auto_reply_message = f'''
        Dear {contact_message.name},
        
        Thank you for reaching out to EIP Ethiopia. We have received your message and will get back to you within 2-3 business days.
        
        Here's a copy of your message:
        Subject: {contact_message.subject}
        Message: {contact_message.message}
        
        Best regards,
        EIP Ethiopia Team
        '''

        send_mail(
            auto_reply_subject,
            auto_reply_message,
            settings.DEFAULT_FROM_EMAIL,
            [contact_message.email],
            fail_silently=True,
        )


@csrf_exempt
@require_POST
def api_contact(request):
    """API endpoint for AJAX contact form submission"""
    try:
        data = json.loads(request.body)

        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'error': f'{field} is required'}, status=400)

        # Create contact message
        contact_message = ContactMessage.objects.create(
            name=data['name'],
            email=data['email'],
            subject=data['subject'],
            message=data['message'],
        )

        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            contact_message.ip_address = x_forwarded_for.split(',')[0]
        else:
            contact_message.ip_address = request.META.get('REMOTE_ADDR')
        contact_message.save()

        # TODO: Send email notification

        return JsonResponse({
            'message': 'Thank you for your message! We will get back to you soon.',
            'status': 'success'
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)
