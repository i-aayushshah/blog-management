from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from apps.core.models import BaseModel
from apps.authentication.models import User


class Category(BaseModel):
    """
    Blog category model for organizing posts.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Category Name')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Category Slug')
    description = models.TextField(blank=True, null=True, verbose_name='Description')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get the absolute URL for the category."""
        return reverse('blog:category_detail', kwargs={'slug': self.slug})

    @property
    def post_count(self):
        """Get the number of published posts in this category."""
        return self.posts.filter(status='published').count()


class Tag(BaseModel):
    """
    Blog tag model for tagging posts.
    """
    name = models.CharField(max_length=50, unique=True, verbose_name='Tag Name')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Tag Slug')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get the absolute URL for the tag."""
        return reverse('blog:tag_detail', kwargs={'slug': self.slug})

    @property
    def post_count(self):
        """Get the number of published posts with this tag."""
        return self.posts.filter(status='published').count()


class Post(BaseModel):
    """
    Blog post model with all required fields and relationships.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200, verbose_name='Post Title')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Post Slug')
    content = models.TextField(verbose_name='Post Content')
    excerpt = models.TextField(blank=True, null=True, verbose_name='Post Excerpt')

    # Relationships
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Author'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Category'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts',
        verbose_name='Tags'
    )

    # Status and metadata
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Post Status'
    )
    featured_image = models.ImageField(
        upload_to='blog_images/',
        blank=True,
        null=True,
        verbose_name='Featured Image'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='Published At')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['author']),
            models.Index(fields=['category']),
            models.Index(fields=['created_at']),
            models.Index(fields=['published_at']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Auto-generate slug from title if not provided.
        """
        if not self.slug:
            self.slug = slugify(self.title)

            # Handle duplicate slugs
            counter = 1
            original_slug = self.slug
            while Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        # Auto-generate excerpt if not provided
        if not self.excerpt and self.content:
            self.excerpt = self.content[:150] + '...' if len(self.content) > 150 else self.content

        # Set published_at if status is published and not already set
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get the absolute URL for the post."""
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    @property
    def is_published(self):
        """Check if the post is published."""
        return self.status == 'published'

    @property
    def reading_time(self):
        """Estimate reading time in minutes (average 200 words per minute)."""
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))

    @property
    def excerpt_or_content(self):
        """Get excerpt if available, otherwise first 150 characters of content."""
        if self.excerpt:
            return self.excerpt
        return self.content[:150] + '...' if len(self.content) > 150 else self.content

    def get_related_posts(self, limit=5):
        """Get related posts based on category and tags."""
        related_posts = Post.objects.filter(status='published').exclude(id=self.id)

        if self.category:
            related_posts = related_posts.filter(category=self.category)

        if self.tags.exists():
            related_posts = related_posts.filter(tags__in=self.tags.all())

        return related_posts.distinct()[:limit]

    def get_next_post(self):
        """Get the next published post."""
        return Post.objects.filter(
            status='published',
            created_at__lt=self.created_at
        ).order_by('-created_at').first()

    def get_previous_post(self):
        """Get the previous published post."""
        return Post.objects.filter(
            status='published',
            created_at__gt=self.created_at
        ).order_by('created_at').first()
