from django.core.mail import send_mail
from django.conf import settings
from core.utils.email import send_contact_notification, send_contact_auto_reply
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ContactMessage
from .forms import ContactForm
import json


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

        # Send email notifications
        try:
            # Send notification to admin
            send_contact_notification(contact_message)

            # Send auto-reply to user
            send_contact_auto_reply(contact_message)

        except Exception as e:
            # Log error but don't crash the form submission
            print(f"Email sending failed: {e}")

        messages.success(
            self.request,
            'Thank you for your message! We have sent a confirmation email to your address and will get back to you soon.'
        )

        return super().form_valid(form)


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

        # Send email notifications
        try:
            send_contact_notification(contact_message)
            send_contact_auto_reply(contact_message)
        except Exception as e:
            # Log but don't fail the API response
            print(f"Email sending failed: {e}")

        return JsonResponse({
            'message': 'Thank you for your message! We have sent a confirmation email and will get back to you soon.',
            'status': 'success'
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)
