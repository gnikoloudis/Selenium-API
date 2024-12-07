import json

# Load JSON configuration files
def load_json(file_name):
    try:
        with open(file_name) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save JSON configuration files
def save_json(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)
