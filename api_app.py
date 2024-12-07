from flask import Flask, request, jsonify
import re
import requests
import pandas as pd
import json

app = Flask(__name__)

# Helper functions (from your provided code)
def send_post_request(url, command, method, selector,text):
    data = {
        "command": command,
        "params": {
            "text": text,
            "method": method,
            "selector": selector
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_product_data(url):
    product_title = send_post_request(url = url, command = "find_all", method = "class", selector = "product__title",text = "")
    product_price = send_post_request(url = url, command ="find_all", method = "class", selector = "price",text = "")
    product_price_unit = send_post_request(url = url, command ="find_all", method = "class", selector = "priceKil",text = "")
    if product_title and product_price and product_price_unit:
        return {
            'Product Name': product_title['command_result']['elements'],
            'Price per Unit': product_price_unit['command_result']['elements'],
            'Product Price': product_price['command_result']['elements']
        }
    else:
        return None

def fetch_products_with_name(url, product_name):
    product_data = fetch_product_data(url)
    if not product_data:
        return []
    try:
        product_names = product_data['Product Name']
        product_prices = product_data['Product Price']
        price_per_unit = product_data['Price per Unit']
        pattern = re.compile(re.escape(product_name), re.IGNORECASE)
        matching_products = []
        for i, name in enumerate(product_names):
            if pattern.search(name):
                matching_products.append({
                    'Product Name': product_names[i],
                    'Product Price': product_prices[i],
                    'Price per Unit': price_per_unit[i]
                })
        return matching_products
    except Exception as e:
        return []
   

def search_products_with_name(url, product_name):

    search_status = send_post_request(url,command = "search",method = "id", selector = "search", text = product_name)

    if search_status==200:
        product_data = fetch_product_data(url)
        if not product_data:
            return []
        try:
            product_names = product_data['Product Name']
            product_prices = product_data['Product Price']
            price_per_unit = product_data['Price per Unit']
            pattern = re.compile(re.escape(product_name), re.IGNORECASE)
            matching_products = []
            for i, name in enumerate(product_names):
                if pattern.search(name):
                    matching_products.append({
                        'Product Name': product_names[i],
                        'Product Price': product_prices[i],
                        'Price per Unit': price_per_unit[i]
                    })
            return matching_products
        except Exception as e:
            return []
    else:
        return "Error"

# Flask route to fetch products by name
@app.route('/fetch_products', methods=['GET'])
def fetch_products():
    """
    Flask endpoint to fetch products matching a specific name.
    Query parameter: name (str) - The product name to search for.

    Example: /fetch_products?name=Παγωτό
    """
    product_name = request.args.get('name')  # Get the product name from query params
    if not product_name:
        return jsonify({"error": "Missing required parameter: name"}), 400

    # Define the URL of the Flask API endpoint
    
    api_url = "http://127.0.0.1:5000/execute"
    
    # Fetch products matching the name
    products = fetch_products_with_name(api_url, product_name)
    
    if products:
        return jsonify(products)
    else:
        return jsonify({"message": f"No products found containing '{product_name}'"}), 404

@app.route('/test_req', methods=['GET'])
def test_req():
    print(request.__dict__)
    return(jsonify("End"))

@app.route('/search_products', methods=['POST'])
def search_products():
    """
    Flask endpoint to fetch products matching a specific name.
    Query parameter: name (str) - The product name to search for.

    Example: /search_products?name=Παγωτό
    """
    product_name = request.form.get('name')  # Get the product name from query params
    print(product_name)
    print(request.__dict__)
    if not product_name:
        return jsonify({"error": "Missing required parameter: name"}), 400

    # Define the URL of the Flask API endpoint
    
    api_url = "http://127.0.0.1:5000/execute"
    
    # Fetch products matching the name
    products = search_products_with_name(api_url, product_name)
    
    if products:
        return jsonify(products)
    else:
        return jsonify({"message": f"No products found containing '{product_name}'"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
