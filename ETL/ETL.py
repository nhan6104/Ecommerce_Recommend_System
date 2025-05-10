import pandas as pd
import os
import sys
from CRUD import CRUD
import json
from ETL.utils import recursiveDict, recursiveVal
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import seaborn as sns
# conn = sqlite3.connect("sales.db")
# cur = conn.cursor() 
class ETL:
    def __init__(self, db_name):
        self.crud = CRUD(db_name)

    def extract(self, file_name, table_name):
        file_type = file_name.split('.')[-1]
        df = None
        if file_type == 'csv':
            df = pd.read_csv(file_name)


        columns = list(df.columns)
        values = df.values.tolist()

        self.crud.create(table_name, columns)

        for value in values:
            print(type(value))
            self.crud.insert(table_name, columns, value)

    def loadDataFromTable(self, table_name, columns = '*'):
        columns, res = self.crud.read(table_name, columns)
        key_lst = [] # Danh sách các tuple, mỗi tuple chứa tên cột 
        val_lst = [] # Danh sách các tuple, mỗi tuple chứa giá trị ứng với mỗi el trên
        columns_name = [] # Danh sách chứa các cột 
        for product in res:
            keys_tmp_lst = []
            val_tmp_lst = []
            for product_info in zip(columns, product):
                data = json.loads(product_info[1])

                if isinstance(data, dict):
                    temp_val = dict()
                    temp_val[product_info[0]] = data

                    keys, vals = recursiveDict(temp_val)
                    columns_name += keys
                    keys_tmp_lst += keys
                    val_tmp_lst += vals

                else:
                    columns_name += [product_info[0]]
                    keys_tmp_lst += [product_info[0]]
                    val_tmp_lst += [json.dumps(data, ensure_ascii=False)]

            key_lst += [tuple(keys_tmp_lst)]
            val_lst += [tuple(val_tmp_lst)]

        return list(frozenset(columns_name)), key_lst, val_lst
    
    def loadDataToCSV(self, table_name):
        columns_name, key_lst, val_lst = self.loadDataFromTable(table_name)
        data = dict()
        for column in columns_name:
            data[column] = []

        for i in range(len(key_lst)):
            for j in range(len(key_lst[i])):
                key = key_lst[i][j]
                val = val_lst[i][j]
                data[key] += [val]

        max_len = 0
        for column in columns_name:
            max_len = max(max_len, len(data[column]))

        for column in columns_name:
            if len(data[column]) < max_len:
                data[column] += [np.nan]*(max_len - len(data[column]))


        df = pd.DataFrame(data)
        for col in df.columns.to_list():
            for i in range(len(df[col])):
                if  df.loc[i, col] == "\"\"" or df.loc[i, col] == "[]" or df.loc[i, col] == 'null':
                    df.loc[i, col] = np.nan

                if df.loc[i, col] == "false":
                    df.loc[i, col] = 0

                elif df.loc[i, col] == "true":
                    df.loc[i, col] = 1  

                if df[col].dtype in ['int64', 'float64', 'bool']:
                    if np.isnan(df.loc[i, col]) :
                        df.loc[i, col] = 0
            # print(df[col].astype("string") )

        file_name = table_name + '.csv'
        df.to_csv(file_name, index=False, encoding='utf-8-sig')

    def merge_file_csv(self, list_files, des_file_name):
        merged_df = pd.concat([pd.read_csv(f) for f in list_files], ignore_index=True)
        merged_df.to_csv(f"{des_file_name}.csv", index=False)


if __name__ == '__main__':
    etl = ETL('product') # connect ETL tool to product database


    lst_files_csv = [table[0] + '.csv'  for table in etl.crud.getTables()]
    etl.merge_file_csv(lst_files_csv, 'product')

    # etl.loadDataToCSV('fashion_accessories_2025_04_16')
    # etl.loadDataToCSV('fashion_accessories_2025_04_16')

    # df = pd.read_csv('fashion_accessories_2025_04_16.csv')
    # describe = describeCol(df)
    # matrix = describe.correlationInfo()
    # # # print(val)
  
    # sns.set_theme(style="dark")
    # plt.figure(figsize=(18, 16))

    # # print(matrix)
    # heatmap = sns.heatmap(matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={"label": "test tingg"})
    # heatmap.set_title("test")
    # plt.show()


    # print(etl.describeColumn(df))
    # etl.extract('./amazon.csv', 'sales')
