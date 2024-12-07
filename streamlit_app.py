import streamlit as st
import json
import requests

# Load JSON configuration files
def load_json(file_name, default_data=None):
    try:
        with open(file_name) as f:
            return json.load(f)
    except FileNotFoundError:
        return default_data if default_data is not None else {}

def save_json(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

# Function to send the command to the Flask API and get the response
def execute_command_via_api(command_name, params):
    url = "http://127.0.0.1:5001/execute"  # Flask API URL
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "command": command_name,
        "params": params
    }
    try:
        # Send POST request to the API
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()  # Return JSON response from the API
        else:
            return {"error": f"API Error: {response.status_code} - {response.text}"}
    except requests.RequestException as e:
        return {"error": str(e)}

# Load configurations
commands_file = 'commands.json'
page_checks_file = 'page_checks.json'
selenium_options_file = 'selenium_options.json'

commands = load_json(commands_file, {"commands": {}})
page_checks = load_json(page_checks_file, {"checks": []})
selenium_options = load_json(selenium_options_file, {})

# Streamlit Tabs
def run_streamlit():
    tab1, tab2, tab3 = st.tabs(["Command Execution", "Manage Configuration", "Selenium Options"])

    # --- Tab 1: Command Execution ---
    with tab1:
        st.title("Selenium Automation with Streamlit")

        st.write("Available Commands:")
        st.json(commands)

        # Input section for the command
        command_name = st.selectbox("Choose a command", options=list(commands["commands"].keys()))

        if command_name:
            params = {}
            for param_name, description in commands["commands"][command_name]["parameters"].items():
                if isinstance(description, list):
                    params[param_name] = st.selectbox(f"Select {param_name}", options=description)
                else:
                    params[param_name] = st.text_input(f"Enter {param_name}")

            # Button to execute the command via the Flask API
            if st.button("Execute Command"):
                st.write(f"Executing command: {command_name} with params: {params}")
                
                # Call the function to execute the command via API
                result = execute_command_via_api(command_name, params)

                # Display the API response
                st.write("Command Result:")
                st.json(result)

    # --- Tab 2: Manage Configuration ---
    with tab2:
        st.title("Manage Configuration Files")

        st.write("Edit and save the configuration files for commands and page checks.")
        
        # Display and edit `commands.json`
        st.subheader("Commands Configuration")
        commands_editor = st.text_area("Commands JSON", value=json.dumps(commands, indent=4), height=400)

        if st.button("Save Commands Configuration"):
            try:
                updated_commands = json.loads(commands_editor)
                save_json(commands_file, updated_commands)
                st.success("Commands configuration saved successfully!")
                commands = updated_commands  # Refresh in memory
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON format: {e}")
        
        # Display and edit `page_checks.json`
        st.subheader("Page Checks Configuration")
        page_checks_editor = st.text_area("Page Checks JSON", value=json.dumps(page_checks, indent=4), height=200)

        if st.button("Save Page Checks Configuration"):
            try:
                updated_page_checks = json.loads(page_checks_editor)
                save_json(page_checks_file, updated_page_checks)
                st.success("Page checks configuration saved successfully!")
                page_checks = updated_page_checks  # Refresh in memory
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON format: {e}")

    # --- Tab 3: Selenium Options ---
    with tab3:
        st.title("Selenium Options Configuration")

        st.write("Configure options for Selenium WebDriver.")

        # Display and edit Selenium options dynamically
        selenium_options_editor = st.text_area("Selenium Options JSON", value=json.dumps(selenium_options, indent=4), height=400)

        if st.button("Save Selenium Options"):
            try:
                updated_selenium_options = json.loads(selenium_options_editor)
                save_json(selenium_options_file, updated_selenium_options)
                st.success("Selenium options saved successfully!")
                selenium_options = updated_selenium_options  # Refresh in memory
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON format: {e}")

# Run the Streamlit app
if __name__ == '__main__':
    run_streamlit()
