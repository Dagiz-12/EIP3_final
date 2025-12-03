from django.db import models
from ckeditor.fields import RichTextField


class PublicationCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Publication(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField()
    category = models.ForeignKey(PublicationCategory, on_delete=models.CASCADE)
    file = models.FileField(upload_to='publications/')
    cover_image = models.ImageField(upload_to='publication_covers/')
    download_count = models.PositiveIntegerField(default=0)
    published_date = models.DateField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_date']
