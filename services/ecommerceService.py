from services.search import recommendSystem
from services.classify import classify_categories_by_name
import pandas as pd

class ecommerceService:
	def __init__(self):
		self.df = pd.read_csv('database/product.csv', low_memory=False)
		self.search_tool = recommendSystem()
		self.classify_tool = classify_categories_by_name()	

	def searchByRecommendSystem(self, query, num_of_products):
		res = []
		docs = self.search_tool.search(query, num_of_products)
		for doc in docs:
			content = doc.page_content
			product_id = content.split(' ')[0]
			# print(type(self.df['id'].iloc[0]))
			product_info = self.df[self.df['id'] == int(product_id)]
			product = {
				'product_id': int(product_info['id'].values[0]),
				'product_brand': product_info['brand_name'].values[0],
				'product_name': product_info['name'].values[0] ,
				'product_image':  product_info['thumbnail_url'].values[0],
				'product_price': int(product_info['original_price'].values[0]),
				'product_type':  product_info['_visible_impression_info_amplitude_category_l1_name'].values[0]
			}
			res.append(product)

		return res


	def classifyProduct(self, product_list, categories = []):
		if len(categories) == 0:
			return product_list
		
		res = []
		for product in product_list:
			nameProduct = product['product_name']
			className = self.classify_tool.classify(nameProduct)
			if className in categories:
				res.append(product)
						
		return res
		
if __name__ == '__main__':
	service = ecommerceService()
	data  = service.searchByRecommendSystem('kính chống ánh sáng xanh', 1)
	print(len(data))