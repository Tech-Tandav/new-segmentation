# News Scraper API

A Django-based REST API that scrapes news articles from OnlineKhabar using Selenium and Celery.

## Quick Start with Docker (Recommended)

1. **Clone and go to the project folder**

2. **Build and run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

   This will start:
   - Django Web Server (http://localhost:8000)
   - Redis (Message Broker)
   - Celery Worker (Background tasks)
   - Celery Beat (Scheduled tasks)

3. **Use the App**

   - **API Endpoint**: `http://localhost:8000/api/news/`
   - **Admin Panel**: `http://localhost:8000/admin/`

4. **Stop**

   ```bash
   docker-compose down
   ```

## Local Development (without Docker)

**Prerequisites**
- Python 3.10+
- Redis Server (must be running locally)
- Chrome & Chromedriver (for Selenium)

**1. Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

**2. Install Dependencies**

```bash
pip install -r requirements.txt
```



**4. Migrations**

```bash
python manage.py migrate
```

**5. Run Services (Terminal Tabs)**

You need to run these in separate terminals:

*Terminal 1: Django Server*
```bash
python manage.py runserver
```

*Terminal 2: Celery Worker*
```bash
celery -A santosh worker -l info
```

*Terminal 3: Celery Beat*
```bash
celery -A santosh beat -l info
```

Open http://127.0.0.1:8000/.

## API Reference

### List & Scrape News

`GET /api/news/`

Fetches news articles. If you provide a `keyword` and no articles are found in the database, it triggers a background scraping task.

**Parameters**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `keyword` | string | Filter by keyword (e.g., `nepal`). Triggers scrape if not found. |
| `date` | string | Filter by date (YYYY-MM-DD). |

**Response (Success)**

```json
[
  {
    "id": 1,
    "title": "Article Title",
    "content": "Full article content...",
    "author": null,
    "published_date": "2023-10-27",
    "source": "OnlineKhabar",
    "url": "https://www.onlinekhabar.com/...",
    "keyword": "politics"
  }
]
```

*Note: If scraping is triggered, the immediate response might be empty. Wait a a few seconds and refresh to see results.*

## Tech Stack

- **Backend**: Django 5, Django REST Framework
- **Scraping**: Selenium (Chrome/Chromedriver)
- **Task Queue**: Celery + Redis
- **Database**: SQLite (default)
- **Deployment**: Docker + Docker Compose

## How the Scraper Works

1. **Search & Filter**: When you request the API with a `keyword` and `date` (e.g., `?keyword=politics&date=2026-02-08`), the system checks the database for articles matching **both** criteria.

2. **Automatic Trigger**: If no articles are found for that specific date, the system automatically triggers a background scraping task for that keyword.

3. **Smart Updates (Re-scraping)**:
   - The scraper searches OnlineKhabar for the keyword.
   - If it finds an article that **already exists** in the database (scraped previously), it **updates** that article's `published_date` to **today**.
   - It also updates the title and content if they have changed.
   - This ensures that if an old article is still a top search result today, it will show up in your "today" filter.
