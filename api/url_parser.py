from dotenv import load_dotenv
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()


def update_url():
    logger.info("chrome запускається...")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.binary_location = "/usr/bin/chromium-browser"

    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(options=chrome_options, service=service)
    driver.set_window_size(1920, 1080)

    wait = WebDriverWait(driver, 10)
    driver.get("https://ap123-illusiondiffusion.hf.space/?view=api")
    url = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'url')]"))
    )
    with open("api/current_url.txt", "w") as file:
        file.write(url.text)
    return url.text
