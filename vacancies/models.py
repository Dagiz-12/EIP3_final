from django.db import models
from ckeditor.fields import RichTextField


class Vacancy(models.Model):
    JOB_TYPES = [
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField()
    requirements = RichTextField()
    responsibilities = RichTextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    location = models.CharField(max_length=200)
    deadline = models.DateField()
    is_published = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']
        verbose_name_plural = "Vacancies"

    def __str__(self):
        return self.title


class Application(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='applications/resumes/')
    additional_documents = models.FileField(
        upload_to='applications/docs/', blank=True)
    applied_date = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(
        null=True, blank=True)  # ADD THIS LINE

    class Meta:
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.full_name} - {self.vacancy.title}"
