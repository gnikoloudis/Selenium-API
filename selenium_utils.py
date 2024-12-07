from selenium import webdriver

# Singleton pattern to store the browser instance
browser_instance = None

def get_browser(selenium_options):
    global browser_instance
    if browser_instance is None:
        # Initialize the WebDriver only once
        browser_instance = start_browser(selenium_options)
    return browser_instance

def start_browser(selenium_options):
    options = webdriver.ChromeOptions()
    
    if selenium_options.get("headless", False):
        options.add_argument("--headless")
    else:
        options.add_argument("--start-maximized")
    
    # Set other options (window size, user-agent)
    prefs = {"profile.default_content_setting_values.geolocation": 2}
    options.add_experimental_option("prefs", prefs)

    for key, value in selenium_options.items():
        if key == "window_size" and value:
            options.add_argument(f"--window-size={value}")
        elif key == "user_agent":
            options.add_argument(f"user-agent={value}")
        elif isinstance(value, bool) and value:
            options.add_argument(f"--{key}")

    # Create WebDriver instance
    browser = webdriver.Chrome(options=options)
    return browser
