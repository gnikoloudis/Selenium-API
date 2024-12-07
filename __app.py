from flask import Flask, request, jsonify
from commands import execute_command
from selenium_utils import get_browser
from config_utils import load_json

# Flask app for the API
app = Flask(__name__)

# Load configurations
commands_file = 'static/commands.json'
page_checks_file = 'static/page_checks.json'
selenium_options_file = 'static/selenium_options.json'

commands = load_json(commands_file)
page_checks = load_json(page_checks_file)
selenium_options = load_json(selenium_options_file)

@app.route('/execute', methods=['POST'])
def execute_api_command():
    data = request.json
    command_name = data.get('command')
    params = data.get('params')

    if command_name not in commands["commands"]:
        return jsonify({"error": "Command not supported"}), 400
    
    # Get the WebDriver instance (ensure it's a singleton)
    browser = get_browser(selenium_options)

    # Perform page load checks before executing any command
    check_results = check_page_loaded(browser, page_checks)

    # Execute the command
    result = execute_command(browser, command_name, params, commands)
    
    return jsonify({"checks": check_results, "command_result": result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
