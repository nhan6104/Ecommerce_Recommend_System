import pandas as pd
import numpy as np

if __name__ == "__main__":
  items = pd.read_csv('product.csv')
  print(items.columns.tolist())
  # print(items[["id", "name"]])

  items[ "_visible_impression_info_amplitude_category_l1_name"] =  items["_visible_impression_info_amplitude_category_l1_name"].apply(lambda x: x.strip('"'))
  items[ "name"] =  items["name"].apply(lambda x: x.strip('"'))
  items[ "brand_name"] =  items["brand_name"].astype(str).apply(lambda x: "no brand" if x == 'nan' else x)

  items[ "brand_name"] =  items["brand_name"].astype(str).apply(lambda x: x.strip('"'))
  items[ "thumbnail_url"] =  items["thumbnail_url"].apply(lambda x: x.strip('"'))
  items.to_csv('product.csv', index=False)
  # items['id_description'].to_csv('id_description.txt', index=False)


  # items['id_description'] =  items[["id", "name"]].astype(str).agg(" ".join, axis=1)
  # items['id_description'].to_csv('id_description.txt', index=False, sep="\n", header=False)
