from celery import shared_task
from .scrapers.onlinekhabar import scrape_onlinekhabar


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 5},
)
def scrape_news_task(self, keyword):
    scrape_onlinekhabar(keyword)
