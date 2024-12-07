from fastapi import Request, FastAPI
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import json


# Load JSON configuration files
def load_json(file_name):
    with open(file_name) as f:
        return json.load(f)

def open_page(driver,url):
    # Define the data payload (command and parameters)

    driver.implicitly_wait(30)
    driver.get(url)
    time.sleep(3)
    driver.quit()

app = FastAPI()

project="sklavenitis"

configuration_file = f'static/{project}/configuration.json'
commands_file = f'static/{project}/commands.json'
page_checks_file = f'static/{project}/page_checks.json'

    
driver = webdriver.Remote(
    command_executor='http://127.0.0.1:4444/wd/hub',
    options=Options()
    )
    

@app.get("/search/{product_name}")
def search(product_name):
    commands = load_json(commands_file)
    page_checks = load_json(page_checks_file)
    url = load_json(configuration_file)["url"]


    status  = open_page(driver,url)

    return({"status":status})

    
