from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def scrape_text_from_url(url):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)  # Let JavaScript load content

        # You can adjust what part of the page you want
        text = driver.find_element("tag name", "body").text
        driver.quit()

        return text
    except Exception as e:
        return f"[Scraper Error] {str(e)}"
