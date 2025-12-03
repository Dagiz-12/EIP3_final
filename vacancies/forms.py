from django import forms
from .models import Application
from django.core.exceptions import ValidationError


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['full_name', 'email', 'phone',
                  'cover_letter', 'resume', 'additional_documents']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'rows': 8,
                'placeholder': 'Why are you interested in this position?'
            }),
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # Check file size (5MB max)
            if resume.size > 5 * 1024 * 1024:
                raise ValidationError("Resume file size must be under 5MB.")

            # Check file extension
            valid_extensions = ['.pdf', '.doc', '.docx']
            if not any(resume.name.lower().endswith(ext) for ext in valid_extensions):
                raise ValidationError(
                    "Unsupported file format. Please upload PDF or Word documents.")

        return resume
