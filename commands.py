
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions  
from selenium.webdriver.common.keys import Keys
from time import time

# Function to execute a command
def execute_command(browser, command_name, params):
    try:
        if command_name == "open":
            browser.session_id =params["session_id"]
            browser.get(params["url"])
            return {"Status":"200","message": f"Opened URL: {params['url']}"}
        
        elif command_name == "search":
            name = params["name"]
            method = params["method"]
            selector = params["selector"]
            browser.session_id =params["session_id"]
            if method == "id":
                element = browser.find_element(By.ID, selector)
            elif method == "class":
                element = browser.find_element(By.CLASS_NAME, selector)
            elif method == "name":
                element = browser.find_element(By.NAME, selector)
            elif method == "xpath":
                element = browser.find_element(By.XPATH, selector)
            
            element.clear()
            element.send_keys(name)
            element.submit()
            sleep(2)
            scroll_pause_time = 5
            scroll_amount = 500
            scroll_up_and_down(browser,scroll_pause_time,scroll_amount)
            return {"Status":"200"}
             
        
        elif command_name == "find":
            method = params["method"]
            selector = params["selector"]
            if method == "id":
                element = browser.find_element(By.ID, selector)
            elif method == "class":
                element = browser.find_element(By.CLASS_NAME, selector)
            elif method == "name":
                element = browser.find_element(By.NAME, selector)
            elif method == "xpath":
                element = browser.find_element(By.XPATH, selector)
            
            return {"message": f"Found element by {method}: {selector}", "text": element.text}

        elif command_name == "click":
            method = params["method"]
            selector = params["selector"]
            if method == "id":
                element = browser.find_element(By.ID, selector)
            elif method == "class":
                element = browser.find_element(By.CLASS_NAME, selector)
            elif method == "name":
                element = browser.find_element(By.NAME, selector)
            elif method == "xpath":
                element = browser.find_element(By.XPATH, selector)
            element.click()
            return {"message": f"Clicked element by {method}: {selector}"}

        elif command_name == "input":
            text = params["text"]
            method = params["method"]
            selector = params["selector"]
            if method == "id":
                element = browser.find_element(By.ID, selector)
            elif method == "class":
                element = browser.find_element(By.CLASS_NAME, selector)
            elif method == "name":
                element = browser.find_element(By.NAME, selector)
            elif method == "xpath":
                element = browser.find_element(By.XPATH, selector)
            elif method == "css_selector":
                element = browser.find_element(By.CSS_SELECTOR, selector)
            element.clear()
            element.send_keys(text)
            element.submit()
            return {"message": f"Entered text '{text}' in element by {method}: {selector}"}
    
    
        elif command_name == "input_id":
            text = params["text"]
            method = params["method"]
            selector = params["selector"]
            if method == "css_selector":
                element = browser.find_element(By.CSS_SELECTOR, selector)
                browser.execute_script(f"arguments[0].setAttribute('id', '{text}')", element)
            element.clear()
            element.send_keys(text)
            return {"message": f"Entered text '{text}' in element by {method}: {selector}"}


        # New command to find all elements by class
        elif command_name == "find_all":
            method = params["method"]
            selector = params["selector"]
            if method == "class":
                elements = browser.find_elements(By.CLASS_NAME, selector)
            element_texts = [element.text for element in elements]
            return {
                "message": f"Found {len(elements)} elements with class '{selector}'",
                "elements": element_texts
            }
        
        # New commands scroll down the page until end 
        elif command_name == "scroll-down":

            browser.session_id =params["session_id"]
            scroll_pause_time = 5
            scroll_amount = 500
            scroll_up_and_down(browser,scroll_pause_time,scroll_amount)
            
            return({"message": "Scrolled down the page"})

        
        elif command_name == "scroll_up":
            scroll_pause_time = params["scroll_pause_time"]
            scroll_amount = params["scroll_amount"]
            scroll_up_and_down(browser,scroll_pause_time,scroll_amount)

        else:
            return {"error": "Unsupported command"}

    except Exception as e:
        return {"error": f"Failed to execute {command_name}: {e}"}


def scroll_up_and_down(browser, scroll_pause_time=1, scroll_amount=500):
    """
    Scroll down and slightly up the page to ensure all content loads.

    Args:
    - driver: Selenium WebDriver instance.
    - scroll_pause_time: Time to wait after each scroll.
    - scroll_amount: The amount to scroll up before scrolling down.
    """
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        browser.implicitly_wait(5)
        # Scroll up a bit before scrolling down (helps to load content in stuck cases)
        browser.execute_script(f"window.scrollBy(0, -{scroll_amount});")
        sleep(scroll_pause_time / 2)  # Wait briefly before scrolling down
        
        # Scroll down to the bottom of the page
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(scroll_pause_time)  # Pause to let content load

        # Calculate new scroll height and check if it has changed
        new_height = browser.execute_script("return document.body.scrollHeight")
        
        # If the scroll height hasn't changed, we assume the page is fully loaded
        if new_height == last_height:
            break

        last_height = new_height  # Update the last height for the next loop



# Function to perform page load checks, return True or False for success/failure
def check_page_loaded(browser, checks):
    results = []
    for check in checks["checks"]:
        try:
            if check["method"] == "id":
                element = browser.find_element(By.ID, check["selector"])
            elif check["method"] == "class":
                element = browser.find_element(By.CLASS_NAME, check["selector"])
            else:
                results.append({"status": "failure", "check": check["description"]})
                continue  # Unsupported method, mark as failure
            results.append({"status": "success", "check": check["description"]})
        except Exception as e:
            results.append({"status": "failure", "check": check["description"], "error": str(e)})
    
    return results
