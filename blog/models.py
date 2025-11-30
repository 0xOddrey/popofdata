from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    featured_image = models.URLField(max_length=500)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    author = models.CharField(max_length=100, default="Audrey Taylor-Akwenye")
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Pop-of-Data")
    tagline = models.CharField(max_length=200, default="Data Science for Pop Culture")
    hero_image = models.URLField(max_length=500, blank=True)
    favicon = models.URLField(max_length=500, blank=True)
    logo = models.URLField(max_length=500, blank=True)
    author_name = models.CharField(max_length=100, default="Audrey Taylor-Akwenye")
    author_title = models.CharField(max_length=200, default="Data Scientist, Educator, Entrepreneur")
    author_image = models.URLField(max_length=500, blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name
