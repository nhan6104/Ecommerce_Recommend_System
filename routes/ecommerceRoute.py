from flask import Blueprint, jsonify, request
from services.ecommerceService import ecommerceService 
import json

ecommerce_route = Blueprint('user', __name__, url_prefix='/users')
service = ecommerceService()
# Create - POST
@ecommerce_route.route('/search', methods=['GET', 'OPTIONS'])
def search_product():
    try:
        query = request.args.get('query')

        products = service.searchByRecommendSystem(query, 20)
        print(products)
        return jsonify({
            "message": "Get product successfully", 
            "products": products
        }), 200
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 400

# Read - GET all users
@ecommerce_route.route('/sort', methods=['POST'])
def sort_product():
    try:
      data = request.get_json()
      categories = data.get('categories')
      products = data.get('products')
    
      products = service.classifyProduct(products, categories)
      print(type(json.dumps(products)))
      return jsonify({
              "message": "Sort product successfully", 
              "products": products
          }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
