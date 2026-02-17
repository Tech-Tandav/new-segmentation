from django.db import models

# Create your models here.
from django.db import models


class NewsArticle(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    author = models.CharField(max_length=255, null=True, blank=True)
    published_date = models.DateField()
    source = models.CharField(max_length=100)
    url = models.URLField(unique=True)
    keyword = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
