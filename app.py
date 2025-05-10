import logging
import sys
from flask import Flask
from flask_cors import CORS
from routes.ecommerceRoute import ecommerce_route

def create_app():
  app = Flask(__name__)
  
  CORS(app, origins=['http://localhost:3000']) # Enabling CORS 
  # CORS(app, origins="*", supports_credentials=True)
  # logging.basicConfig(filename = 'app.log', level = logging.DEBUG)

  app.register_blueprint(ecommerce_route)

  return app

app = create_app()

if __name__ == '__main__':
  app.run(host='127.0.0.1', port = 3001, debug=True)