from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Setup Firefox options (headless mode optional)
options = Options()
options.add_argument("--headless")  # Uncomment to run in headless mode

geckodriver_path = "/snap/bin/geckodriver"

# Set up the Firefox WebDriver
service = webdriver.ChromeService(executable_path=geckodriver_path)  # Uses geckodriver from PATH
driver = webdriver.Chrome(service=service, options=options)


def connect_to_url_with_selenium(target_url):
    result = None
    try:
        # Navigate to the URL
        driver.get(target_url)
        # Wait a moment for page to load (if needed)
        time.sleep(1)
        result = driver
        driver.quit()
    except Exception as e: 
        print(e) 
    
    return result 

    
if __name__ == "__name__":
    print(connect_to_url_with_selenium("https://www.monergism.com/topics"))