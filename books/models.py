from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Create your models here.
class Books(models.Model):
    streaming_choices = (('AK', 'Amazon Kindle'), ('PB', 'Physical Book'))
    name = models.CharField(max_length=50)
    streaming = models.CharField(max_length=2, choices = streaming_choices)
    grade = models.IntegerField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Categories)

    def __str__(self):
        return self.name
