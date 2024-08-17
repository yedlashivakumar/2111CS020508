from flask import Flask, request, jsonify
import requests
import uuid
app = Flask(__name__)
TEST_SERVER_URL = "http://20.244.56.144/test/companies"
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzIzODc3OTM5LCJpYXQiOjE3MjM4Nzc2MzksImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjhmMzIzYTIzLWEzYWEtNDlhNS1iZDM5LTFjZDc1NWEyYWFjNyIsInN1YiI6IjIxMTFjczAyMDUwOEBtYWxsYXJlZGR5dW5pdmVyc2l0eS5hYy5pbiJ9LCJjb21wYW55TmFtZSI6Ik1hbGxhIFJlZGR5IFVuaXZlcnNpdHkiLCJjbGllbnRJRCI6IjhmMzIzYTIzLWEzYWEtNDlhNS1iZDM5LTFjZDc1NWEyYWFjNyIsImNsaWVudFNlY3JldCI6IkNSdWtxclBmQnBPd1ZiWW8iLCJvd25lck5hbWUiOiJTaGl2YSBLdW1hciBZZWRsYSIsIm93bmVyRW1haWwiOiIyMTExY3MwMjA1MDhAbWFsbGFyZWRkeXVuaXZlcnNpdHkuYWMuaW4iLCJyb2xsTm8iOiIyMTExQ1MwMjA1MDgifQ.9kZAXESdrxAYYngoWDD1ixbVv30Jark_5o094E028J8"
COMPANIES = ["ARZ", "FLP", "SA", "MMI", "AZO"]
CATEGORIES = ["Phone", "Computer", "TV", "Earphone", "Tablet", "Charger", "House", "Keypad", "Bluetooth", "Pendrive", "Remote", "Speaker", "Headset", "Laptop"]
def fetch_products(company, category, top, min_price, max_price):
    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN}'
    }
    url = f"{TEST_SERVER_URL}/{company}/categories/{category}/products?top={top}&minPrice={min_price}&maxPrice={max_price}"
    print(f"Fetching URL: {url}") 
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        app.logger.error(f"Failed to fetch products from {company}: {response.status_code}")
        return []
def generate_product_id():
    return str(uuid.uuid4())
@app.route('/categories/<category>/products', methods=['GET'])
def get_products(category):
    if category not in CATEGORIES:
        return jsonify({'error': 'Invalid category'}), 400
    try:
        top = int(request.args.get('top', 10))
        page = int(request.args.get('page', 1))
        sort_by = request.args.get('sort_by', 'rating')
        order = request.args.get('order', 'desc')
        min_price = float(request.args.get('minPrice', 0))
        max_price = float(request.args.get('maxPrice', 10000))
    except ValueError:
        return jsonify({'error': 'Invalid query parameters'}), 400
    if top > 10:
        top = 10
    offset = (page - 1) * top
    all_products = []
    for company in COMPANIES:
        products = fetch_products(company, category, top + offset, min_price, max_price)
        all_products.extend(products)
    if sort_by in ['price', 'rating', 'discount']:
        all_products.sort(key=lambda x: x.get(sort_by, 0), reverse=(order == 'desc'))

    for product in all_products:
        product['productId'] = generate_product_id()

    paginated_products = all_products[offset:offset + top]

    return jsonify(paginated_products)

@app.route('/categories/<category>/products/<product_id>', methods=['GET'])
def get_product_details(category, product_id):
    if category not in CATEGORIES:
        return jsonify({'error': 'Invalid category'}), 400

    for company in COMPANIES:
        products = fetch_products(company, category, 100, 0, 10000)
        for product in products:
            if product.get('productId') == product_id:
                return jsonify(product)
    
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '_main_':
    port = 5000
    print(f"Running Flask app on port {port}")
    app.run(port=port, debug=True)