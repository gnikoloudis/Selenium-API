from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time 



chrome_options = webdriver.ChromeOptions( )

chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36')
chrome_options.add_argument("--no-sandbox")


driver = webdriver.Remote(
   command_executor='http://127.0.0.1:4444/wd/hub',
   options=chrome_options
)



driver.implicitly_wait(30)
driver.get("https://google.com")
time.sleep(3)
driver.quit()