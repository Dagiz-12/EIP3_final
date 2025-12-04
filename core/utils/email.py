from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_contact_notification(contact_message):
    """Send email notification to admin about new contact message"""
    subject = f'New Contact Message: {contact_message.subject}'

    # Create HTML context
    context = {
        'name': contact_message.name,
        'email': contact_message.email,
        'subject': contact_message.subject,
        'message': contact_message.message,
        'date': contact_message.created_date,
        'ip_address': contact_message.ip_address,
        'admin_url': f'{settings.SITE_URL}/admin/contacts/contactmessage/{contact_message.id}/change/',
    }

    # Render HTML content
    html_content = render_to_string(
        'emails/contact_notification.html', context)
    text_content = strip_tags(html_content)

    # Send email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.ADMIN_EMAIL],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)


def send_contact_auto_reply(contact_message):
    """Send auto-reply to user who submitted contact form"""
    subject = f'Thank you for contacting EIP Ethiopia'

    context = {
        'name': contact_message.name,
        'subject': contact_message.subject,
        'message': contact_message.message,
    }

    html_content = render_to_string('emails/contact_auto_reply.html', context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[contact_message.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)


def send_application_notification(application):
    """Send notification about new job application"""
    subject = f'New Application: {application.vacancy.title}'

    context = {
        'vacancy_title': application.vacancy.title,
        'applicant_name': application.full_name,
        'applicant_email': application.email,
        'applicant_phone': application.phone,
        'cover_letter': application.cover_letter,
        'applied_date': application.applied_date,
        'ip_address': application.ip_address,
        'resume_url': application.resume.url if application.resume else '',
        'additional_docs_url': application.additional_documents.url if application.additional_documents else '',
        'admin_url': f'{settings.SITE_URL}/admin/vacancies/application/{application.id}/change/',
    }

    html_content = render_to_string(
        'emails/application_notification.html', context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.ADMIN_EMAIL],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)


def send_application_confirmation(application):
    """Send confirmation email to job applicant"""
    subject = f'Application Received: {application.vacancy.title}'

    context = {
        'applicant_name': application.full_name,
        'vacancy_title': application.vacancy.title,
        'applied_date': application.applied_date,
        'deadline': application.vacancy.deadline,
    }

    html_content = render_to_string(
        'emails/application_confirmation.html', context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[application.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)
