from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def scrape_text_from_url(url):
    driver = None
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Better approach than sleep: wait for body element
        time.sleep(3)
        text = driver.find_element(By.TAG_NAME, "body").text
        return text

    except Exception as e:
        return f"[Scraper Error] {str(e)}"
    finally:
        if driver:
            driver.quit()
