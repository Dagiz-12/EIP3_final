from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from .models import ContactMessage, Subscriber


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your email address'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 6,
                'placeholder': 'Your message...'
            }),
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message.strip()) < 10:
            raise ValidationError(
                "Message must be at least 10 characters long.")
        return message


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your email'
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Please enter a valid email address.")

        # Check for disposable email
        disposable_domains = ['tempmail.com', 'throwaway.com']  # Add more
        domain = email.split('@')[-1]
        if domain in disposable_domains:
            raise ValidationError(
                "Disposable email addresses are not allowed.")

        return email
