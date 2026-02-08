from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import NewsArticle
from .serializers import NewsArticleSerializer

from news.tasks import scrape_news_task


class NewsListAPIView(APIView):
    def get(self, request):
        keyword = request.query_params.get("keyword")
        date = request.query_params.get("date")

        queryset = NewsArticle.objects.all()

        if keyword:
            queryset = queryset.filter(keyword__icontains=keyword)

        if date:
            queryset = queryset.filter(published_date=date)

        queryset = queryset.order_by("-published_date")[:10]

        # Trigger scraping if no data
        if keyword and not queryset.exists():
            scrape_news_task.delay(keyword)

        serializer = NewsArticleSerializer(queryset, many=True)
        return Response(serializer.data)
