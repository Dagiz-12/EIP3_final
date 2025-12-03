from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django_resized import ResizedImageField

class SliderImage(models.Model):
    title = models.CharField(max_length=200)
    image = ResizedImageField(size=[1920, 1080], quality=90, upload_to='slider/')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    link = models.URLField(blank=True)
    
    class Meta:
        ordering = ['order']

class GuidingPrinciple(models.Model):
    title = models.CharField(max_length=200)
    icon = models.CharField(max_length=100, help_text="FontAwesome icon class")
    description = RichTextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']

class Partner(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partners/')
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

class BoardMember(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    photo = ResizedImageField(size=[400, 400], quality=85, upload_to='board/')
    bio = RichTextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']

class Strategy(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField()
    icon = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']