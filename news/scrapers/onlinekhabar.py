from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from news.models import NewsArticle
from datetime import date
import time

def scrape_onlinekhabar(keyword):
    # 1. SETUP THE TOOLS (DOCKER STYLE)
    options = Options()
    
    # "Headless" is mandatory in Docker because there is no monitor/screen
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox") # Prevents permission issues in Linux/Docker
    options.add_argument("--disable-dev-shm-usage") # Prevents memory crashes
    
    # Point to the Chromium we installed in the Dockerfile
    options.binary_location = "/usr/bin/chromium" 

    # Point to the Driver we installed in the Dockerfile
    service = Service("/usr/bin/chromedriver")

    # Start the browser (The "Driver")
    driver = webdriver.Chrome(service=service, options=options)

    # 2. THE SEARCH
    search_url = f"https://www.onlinekhabar.com/?s={keyword.replace(' ', '+')}"
    driver.get(search_url)
    time.sleep(3) # Let the site "wake up"

    # 3. SELECTING THE LINKS
    # Limit to 10 so we don't scrape the whole internet at once
    elements = driver.find_elements(By.CSS_SELECTOR, ".search-results-append .ok-news-post a")[:10]
    print(f"Found {len(elements)} articles")
    
    article_urls = [el.get_attribute("href") for el in elements if el.get_attribute("href")]

    # 4. DATA MINING
    for url in article_urls:
        driver.get(url)
        time.sleep(2) # Give it 2 seconds to load the text

        try:
            # Get the Title and Content
            title = driver.find_element(By.TAG_NAME, "h1").text
            # Note: OnlineKhabar uses 'ok-main-content' or 'entry-content'
            content = driver.find_element(By.CLASS_NAME, "ok18-single-post-content-wrap").text 
        except Exception as e:
            print(f"Failed to extract {url}: {e}")
            continue
        
        # 5. SAVE OR UPDATE DATABASE
        # Check if exists to update, or create new
        # We want to update the DATE if we find it again today
        NewsArticle.objects.update_or_create(
            url=url,
            defaults={
                "title": title,
                "content": content,
                "published_date": date.today(),
                "source": "OnlineKhabar",
                "keyword": keyword,
            }
        )
        print(f"Saved/Updated: {title[:30]}...")

    # 6. SHUT DOWN THE BROWSER
    driver.quit()