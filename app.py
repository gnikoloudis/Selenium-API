from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from  commands import execute_command, check_page_loaded
import sys

# Flask app for the API
app = Flask(__name__)

# Load JSON configuration files
def load_json(file_name):
    with open(file_name) as f:
        return json.load(f)

def save_json(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

# Initialize Selenium WebDriver dynamically based on options in selenium_options.json
def start_browser(selenium_options):
    
    options = webdriver.ChromeOptions( )
    prefs = {
            #"profile.default_content_setting_values.geolocation": 2,
            #"download.default_directory" : "C:\\Users\\georg\\Python Projects\\Selenium API\\promitheus"
            };
    
    options.add_experimental_option("prefs", prefs)

    for key, value in selenium_options.items():
        if isinstance(value, bool):
            if value:
                options.add_argument(f"--{key}")
        elif key == "window_size" and value:
            options.add_argument(f"--window-size={value}")
        elif key == "user_agent":
            options.add_argument(f"user-agent={value}")
        else:
            options.add_argument(f"--{key}={value}")

    browser = webdriver.Chrome(options=options)
    return browser


# --- API Section ---
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


# Load configurations

project="sklavenitis"
selenium_options_file = f'static/{project}/selenium_options.json'
configuration_file = f'static/{project}/configuration.json'

selenium_options = load_json(selenium_options_file)
configuration_options = load_json(configuration_file)

for key, value in configuration_options.items():
        if key == "webdriver-path" and value:
            sys.path.append(value)

# Initialize the browser with dynamically configured options
browser = start_browser(selenium_options)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
