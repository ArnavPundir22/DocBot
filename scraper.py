from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_text_from_url(url):
    driver = None
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)

        driver.get(url)

        # ✅ Wait until the <body> tag is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        text = driver.find_element(By.TAG_NAME, "body").text

        return text

    except Exception as e:
        return f"[Scraper Error] {str(e)}"
    finally:
        if driver:
            driver.quit()
