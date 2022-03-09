from selenium import webdriver
import pytest
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

@pytest.fixture
def driver(autouse=True):
    service_object = Service(ChromeDriverManager().install())
    _driver = webdriver.Chrome(service=service_object, options=chrome_options)
    _driver.implicitly_wait(30)
    yield _driver
    _driver.quit()
