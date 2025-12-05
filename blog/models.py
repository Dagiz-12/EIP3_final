from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django_resized import ResizedImageField
import os
import uuid


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=150, blank=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True,
                            help_text="FontAwesome icon class (e.g., fa-newspaper)")
    color = models.CharField(max_length=7, default='#3B82F6',
                             help_text="Hex color for category badge")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def post_count(self):
        return self.post_set.filter(status='published').count()


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, max_length=100, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def post_image_path(instance, filename):
    """Generate safe path for post images even before instance is saved."""
    ext = filename.split('.')[-1]
    obj_id = instance.id or uuid.uuid4().hex[:8]  # Shorter ID for readability
    filename = f"{slugify(instance.title)[:50]}-{obj_id}.{ext}"
    return os.path.join(
        'posts',
        str(timezone.now().year),
        str(timezone.now().month),
        filename
    )


class PostImage(models.Model):
    """Model for images within post content"""
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='content_images')
    image = models.ImageField(upload_to=post_image_path)
    caption = models.CharField(max_length=200, blank=True, null=True)
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Image for {self.post.title}"


class Post(models.Model):
    POST_TYPES = [
        ('news', '📰 News'),
        ('blog', '📝 Blog'),
        ('implementation', '🚀 Implementation & Progress'),
    ]

    POST_STATUS = [
        ('draft', '📝 Draft'),
        ('published', '✅ Published'),
        ('scheduled', '📅 Scheduled'),
        ('archived', '🗄️ Archived'),
    ]

    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=250, blank=True,
                            help_text="URL-friendly version of the title")
    excerpt = models.TextField(max_length=300,
                               help_text="Brief summary for listings and meta descriptions")

    # Content
    content = RichTextField(config_name='default')
    post_type = models.CharField(
        max_length=20, choices=POST_TYPES, default='blog')
    status = models.CharField(
        max_length=20, choices=POST_STATUS, default='draft')

    # Images
    featured_image = models.ImageField(
        upload_to='posts/featured/',
        blank=True,
        null=True,
        help_text="Optional. Main image shown in listings and at top of post"
    )
    featured_image_alt = models.CharField(
        max_length=200, blank=True, null=True)

    # Relationships
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    # Dates
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(
        null=True,  # Make null=True for drafts
        blank=True,
        help_text="Leave empty for drafts. Set for scheduled or published posts."
    )

    # Metadata
    views = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False,
                                      help_text="Feature this post on homepage")
    allow_comments = models.BooleanField(default=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)

    # SEO & Social
    og_title = models.CharField(max_length=200, blank=True, null=True)
    og_description = models.CharField(max_length=300, blank=True, null=True)
    og_image = models.ImageField(upload_to='posts/og/', blank=True, null=True)

    class Meta:
        ordering = ['-published_date', '-created_date']
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['published_date']),
            models.Index(fields=['post_type']),
            models.Index(fields=['status']),
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate slug if empty
        if not self.slug:
            self.slug = slugify(self.title)[:250]

            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        # Handle published date logic
        if self.status == 'published' and not self.published_date:
            # If publishing for first time, set published_date to now
            self.published_date = timezone.now()
        elif self.status in ['draft', 'scheduled']:
            # Keep published_date as is for drafts/scheduled posts
            pass

        super().save(*args, **kwargs)

    @property
    def is_published(self):
        """Check if post is published AND published date is not in future"""
        if self.status != 'published':
            return False
        if not self.published_date:
            return False
        return self.published_date <= timezone.now()

    @property
    def reading_time(self):
        """Estimate reading time without counting HTML tags"""
        text = strip_tags(self.content)
        words = len(text.split())
        return max(1, round(words / 200))  # 200 wpm average

    def increment_views(self):
        """Thread-safe view counter"""
        Post.objects.filter(pk=self.pk).update(views=models.F('views') + 1)
        self.refresh_from_db()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog_detail', kwargs={'slug': self.slug})


class PostView(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post_views')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    referer = models.URLField(blank=True, null=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Post View"
        verbose_name_plural = "Post Views"
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['post', 'viewed_at']),
            models.Index(fields=['viewed_at']),
        ]

    def __str__(self):
        return f"View of {self.post.title} from {self.ip_address}"


# Optional: For tracking popular/most viewed posts over time
class DailyPostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateField()
    views = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['post', 'date']
        verbose_name = "Daily Post View"
        verbose_name_plural = "Daily Post Views"

    def __str__(self):
        return f"{self.post.title} - {self.date}: {self.views} views"
