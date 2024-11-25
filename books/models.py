from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Categories(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

class Books(models.Model):
    streaming_choices = (
        ('AK', 'Amazon Kindle'),
        ('PB', 'Physical Book')
    )
    name = models.CharField(max_length=50, unique=True)
    streaming = models.CharField(max_length=2, choices=streaming_choices)
    grade = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Rating from 0 to 10"
    )
    comments = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Categories, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Books"
        ordering = ['-created_at']