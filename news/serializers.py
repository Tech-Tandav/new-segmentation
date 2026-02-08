from rest_framework import serializers
from .models import NewsArticle
# Serializer converts Django model objects ➝ JSON (and vice-versa).

# ModelSerializer automatically maps model fields.

class NewsArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsArticle
        fields = [
            "id",
            "title",
            "content",
            "author",
            "published_date",
            "source",
            "url",
            "keyword",
        ]
