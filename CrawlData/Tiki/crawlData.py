import requests
from ETL.CRUD import CRUD
from ETL.utils import recursiveDict
from CrawlData.Tiki.config import header
import os
import pandas as pd
import datetime
import json






#     response = requests.get(f"https://tiki.vn/api/v2/products/{product_id}", params = params_product_detail, headers=header)
  
#     params_product_estimate = {
#         'limit': 5,
#         'include': 'comments,contribute_info,attribute_vote_summary',
#         'sort': 'score|desc,id|desc,stars|all',
#         'page': 1,
#         'spid': seller_product_id,
#         'product_id': product_id,
#         'seller_id': response.json().get('current_seller').get('id')
#     }
  
#     comment = requests.get(f"https://tiki.vn/api/v2/reviews", headers=header, params=params_product_estimate)
    
#     print(list(dict(response.json()).keys()) + list(dict(comment.json()).keys()))
#     break

# value = dict(res.json().get('data')[0])
# print(type(value['quantity_sold'])) 


class TikiData:
    def __init__(self):
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path, 'menu.json')
        self.menu = pd.read_json(file_path)
        self.crud_product = CRUD('product')
        self.crud_estimate = CRUD('estimate_product')
        self.product_keys_info = None
        self.estimate_keys_info = None
        

    def crawlProductInfo(self, type_category):
        params = dict(self.menu[type_category])

        table_name = type_category + '_' + str(datetime.datetime.today().date()).replace('-', '_')
        isTable = self.crud_product.checkExistTable(table_name)
        productsResponse = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings', headers=header, params=params)
        if not isTable:
            productsResponse = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings', headers=header, params=params)
            product_list = productsResponse.json().get('data')
            product_keys_info = list(dict(product_list[0]).keys())
            self.crud_product.create(table_name,  product_keys_info)
            isTable = True

        
        paging_product = productsResponse.json().get('paging')
        last_page = paging_product.get('last_page')
        product_list = productsResponse.json().get('data')
        for page in range(1, last_page + 1):
            # crawl product id
            params['page'] = page
            res = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings', headers=header, params=params)
            product_list = res.json().get('data')


            for product in product_list:
                columns = list(dict(product).keys())
                values = list(map(lambda x: json.dumps(x,  ensure_ascii=False), list(dict(product).values())))

                self.crud_product.insert(table_name, columns, values)

        return table_name
              

    def crawlComment(self, table_name_product):
        columns, res = self.crud_product.read(table_name_product, ['id', 'seller_id', 'seller_product_id'])
        isTable = self.crud_estimate.checkExistTable(table_name_product)
        for el in res:
            params = {
                'limit': 5,
                'include': 'comments,contribute_info,attribute_vote_summary',
                'sort': 'score|desc,id|desc,stars|all',
                'page': 1,
                'spid': el[2],
                'product_id': el[0],
                'seller_id': el[1]
            }

            response = requests.get(f"https://tiki.vn/api/v2/reviews", headers=header, params=params)
            
            if not response.json().get('data'):
                continue
            
            if not isTable:
                comment_list = response.json().get('data')
                estimate_keys_info = list(dict(comment_list[0]).keys())
                self.crud_estimate.create(table_name_product, estimate_keys_info)
                isTable = True

            last_page = response.json().get('paging').get('last_page')
            for page in range(1, last_page + 1):
                print(page)
                params['page'] = page
                response = requests.get(f"https://tiki.vn/api/v2/reviews", headers=header, params=params)

                for comment in response.json().get('data'):
                    columns = list(dict(comment).keys())
                    values = list(map(lambda x: json.dumps(x,  ensure_ascii=False), list(dict(comment).values())))

                    self.crud_estimate.insert(table_name_product, columns, values)


    # def miningStructureData(self, type_category):
    #     params = dict(self.menu[type_category])
    #     table_name = type_category + '_' + str(datetime.datetime.today().date()).replace('-', '_')

    #     productsResponse = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings', headers=header, params=params)
    #     product_list = productsResponse.json().get('data')
    #     self.product_keys_info = list(dict(product_list[0]).keys())
    #     self.crud_product.create(table_name,  self.product_keys_info)

        # seller_id =  product_list[0].get('seller_id')
        # product_id = product_list[0].get('id')
        # spid = product_list[0].get('seller_product_id')
        # params_esitmate = {
        #     'limit': 5,
        #     'include': 'comments,contribute_info,attribute_vote_summary',
        #     'sort': 'score|desc,id|desc,stars|all',
        #     'page': 1,
        #     'spid': spid,
        #     'product_id': product_id,
        #     'seller_id': seller_id
        # }

        # response = requests.get(f"https://tiki.vn/api/v2/reviews", headers=header, params=params_esitmate)
        # comment_list = response.json().get('data')
        # if len(comment_list) > 0:
        #     self.estimate_keys_info = list(dict(comment_list[0]).keys())
        #     self.crud_estimate.create(table_name, self.estimate_keys_info)

        # return table_name
    
if __name__ == '__main__':

    data = TikiData()
    print(data.crud_product.getTables())
    tableNames = []
    # for typ in ['book', 'tablet_phone', 'man_shoes', 'woman_fashion', 'woman_shoes']:
    #     tableName = data.crawlProductInfo(typ)
    #     tableNames.append(tableName)
    print("________________________crawl esitmate product___________________________")
    # table = [el[0] for el in data.crud_product.getTables()]
    # print(table)
    for table in ['tablet_phone_2025_04_20', 'man_shoes_2025_04_20', 'woman_fashion_2025_04_20', 'woman_shoes_2025_04_20']:
        data.crawlComment(table)