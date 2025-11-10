from django.db import models
from django.utils import timezone
import math
from django.db.models import Count
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)  # Added image field
    is_hot_topic = models.BooleanField(default=False)  # Added hot topic boolean field

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    profile_image = models.ImageField(upload_to='authors/', blank=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    image = models.ImageField(upload_to='tags/', blank=True, null=True)  # Optional, for tag images

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    draft_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_editors_pick = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)  # <-- Add this line

    def publish(self):
        self.status = 'published'
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    @property
    def read_time(self):
        words = len(self.content.split())
        minutes = math.ceil(words / 200)  # Assuming 200 words per minute
        return f"{minutes} min{'s' if minutes > 1 else ''} to read"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ['-subscribed_at']

class AboutPage(models.Model):
    title = models.CharField(max_length=200, default="About Me", blank=True)
    intro = models.TextField(default="Welcome to my blog! My name is Sakkhar, and I am passionate about sharing knowledge, ideas, and inspiration on technology, travel, lifestyle, and more.", blank=True)
    content_1 = models.TextField(default="I use animation as a third dimension by which to simplify experiences and guide you through each and every interaction. I'm not adding motion just to spruce things up, but doing it in ways that make your experience better.", blank=True)
    content_2 = models.TextField(default="On this blog, you'll find editor's picks, hot topics, and the latest posts from a variety of categories. Whether you're here for tips, reviews, or just to explore, I hope you enjoy your stay!", blank=True)
    resume_file = models.FileField(upload_to='about/', blank=True, null=True, help_text="Upload resume PDF")
    
    def __str__(self):
        return "About Page Content"
    
    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

class ContactPage(models.Model):
    title = models.CharField(max_length=200, default="Contact Me", blank=True)
    description = models.TextField(default="We are a creative and dedicated group of individuals who love web development.", blank=True)
    form_title = models.CharField(max_length=200, default="Drop Us a Line", blank=True)
    form_subtitle = models.CharField(max_length=255, default="Your email address will not be published. Required fields are marked *", blank=True)
    google_map_embed = models.TextField(blank=True, help_text="Google Maps embed URL")
    
    def __str__(self):
        return "Contact Page Content"
    
    class Meta:
        verbose_name = "Contact Page"
        verbose_name_plural = "Contact Page"

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, default="My Website", blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to='site_settings/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='site_settings/', blank=True, null=True)
    
    # Homepage Banner
    banner_greeting = models.CharField(max_length=100, default="Hello Everyone!", blank=True)
    banner_name = models.CharField(max_length=100, default="Your Name", blank=True)
    banner_roles = models.CharField(max_length=255, default='[ "Designer", "Developer", "Creator" ]', blank=True, help_text="JSON format array for typewriter effect")
    banner_description = models.TextField(default="I use animation as a third dimension by which to simplify experiences and guiding through each and every interaction.", blank=True)
    
    # Subscribe Section
    subscribe_placeholder = models.CharField(max_length=100, default="Type your email address", blank=True)
    subscribe_button_text = models.CharField(max_length=50, default="Subscribe", blank=True)
    
    # Homepage Hot Topics
    hot_topics_title = models.CharField(max_length=100, default="Hot topics", blank=True)
    hot_topics_description = models.TextField(default="Don't miss the trending topics", blank=True)
    
    # Portfolio Page Content
    portfolio_title = models.CharField(max_length=200, default="My Latest Projects", blank=True)
    portfolio_description = models.TextField(default="The convention is the main event of the year for professionals in the world of design and architecture.", blank=True)
    
    # Social Media
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)

    def __str__(self):
        return "Site Settings"

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

class PortfolioCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    order = models.IntegerField(default=0, help_text="Display order (lower number appears first)")
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Portfolio Categories"
    
    def __str__(self):
        return self.name

class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='portfolio/')
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True, help_text="Enter category name (e.g., Web Development, Mobile App, etc.)")
    tech_stack = models.CharField(max_length=500, blank=True, help_text="Technologies used (e.g., Django, React, PostgreSQL)")
    link = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while Portfolio.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, help_text="CSS class for the icon (e.g. 'icon-motion')")

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    content = models.TextField()

    def __str__(self):
        return self.name

class Partner(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='partners/')
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Education(models.Model):
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    start_year = models.CharField(max_length=10)
    end_year = models.CharField(max_length=10)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.degree} at {self.institution}"

class Experience(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    start_year = models.CharField(max_length=10)
    end_year = models.CharField(max_length=10)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

# Example for a view or context processor
# from .models import Tag

# tags = Tag.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')[:12]
