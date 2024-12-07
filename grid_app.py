from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from  commands import execute_command, check_page_loaded
import requests
from urllib.parse import urlparse

# Function to initialize the WebDriver
def start_selenium_session():
    global browser
    chrome_options = webdriver.ChromeOptions( )
        

    chrome_options = webdriver.ChromeOptions( )

    chrome_options.add_argument("--disable-extensions")
    #chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36')
    chrome_options.add_argument("--no-sandbox")


    if browser is not None:
        try:
            browser.quit()  # Clean up any existing driver instance
        except:
            pass
    browser = webdriver.Remote(command_executor=GRID_URL, options=chrome_options)
    return browser

# Load JSON configuration files
def load_json(file_name):
    with open(file_name) as f:
        return json.load(f)

def save_json(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

# Initialize Selenium WebDriver dynamically based on options in selenium_options.json
def start_browser():
    global browser

    chrome_options = webdriver.ChromeOptions( )

    chrome_options.add_argument("platformName", "Windows")
    chrome_options.add_argument("se:name", "Supermarket") 
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument(f"--user_agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36")
    chrome_options.add_argument("--no-sandbox")
    if browser is not None:
        try:
            browser.quit()  # Clean up any existing driver instance
        except:
            pass
    
    browser = webdriver.Remote(
        command_executor=GRID_URL,
        options=chrome_options
    )
    
    return browser

# Function to check session status
def is_session_active():
    global browser
    try:
        if browser and browser.session_id:  # Check if the driver exists and has a session_id
            # Make a request to the WebDriver server to verify the session is still active
            response = requests.get(f"{GRID_URL}/session/{browser.session_id}")
            return response.status_code == 200
    except Exception:
        pass
    return False

def is_valid_url(url):
    """
    Validate if the given URL is valid.
    
    Args:
    - url (str): The URL to validate.
    
    Returns:
    - bool: True if the URL is valid, False otherwise.
    """
    try:
        result = urlparse(url)
        # A valid URL must have a scheme (e.g., http/https) and a netloc (e.g., domain.com)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


# ---  Flask app for the API ---#
browser = None

app = Flask(__name__)

project="sklavenitis"

# Load configurations

selenium_options_file = f'static/{project}/selenium_options.json'

configuration_file = f'static/{project}/configuration.json'

selenium_options = load_json(selenium_options_file)

configuration_options = load_json(configuration_file)

GRID_URL = configuration_options['grid_url']


# --- API Section ---

# Clean up on Flask shutdown
@app.route('/stop_session', methods=['GET'])
def stop_session():
    global browser
    if browser:
        browser.quit()
    return jsonify({"status": "Shutdown complete"})

# Endpoint to trigger Selenium and ensure session is active
@app.route('/trigger', methods=['GET'])
def trigger_selenium():
    global browser

    url = request.args.get('url')
    if is_valid_url(url)==True:
        # Check if the session is active, and restart if not
        if not is_session_active():
            browser = start_selenium_session()

        # Example Selenium action
        browser.get(url)
        return jsonify({"title": browser.title})
    else:
        return jsonify({"Error": "Invalid url"})


@app.route('/start_session', methods=['GET'])
def start():
    global browser
    # Check if the session is active, and restart if not
    if not is_session_active():
        browser = start_selenium_session()
        browser.get("https://www.sklavenitis.gr")
        return jsonify({"Started": True,
                        "session_id": browser.session_id})
    

@app.route('/execute', methods=['POST'])
def execute_api_command():
    
    commands_file = f'static/{project}/commands.json'
    page_checks_file = f'static/{project}/page_checks.json'

    commands = load_json(commands_file)
    page_checks = load_json(page_checks_file)

    data = request.json
    command_name = data.get('command')
    params = data.get('params')
    if command_name not in commands["commands"]:
        return jsonify({"error": "Command not supported"}), 400
    
    # Perform page load checks before executing any command
    check_results = check_page_loaded(browser, page_checks)
    result = execute_command(browser, command_name, params)
    return jsonify({"checks": check_results, "command_result": result})




if __name__ == '__main__':
    start_selenium_session()  # Start a session when the app starts
    app.run(host="0.0.0.0", port=5000)
    
