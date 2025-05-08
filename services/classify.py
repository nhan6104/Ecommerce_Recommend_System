# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
import gensim
from pyvi import ViTokenizer
import pickle
import json

class classify_categories_by_name:
	def __init__(self):
		with open('models/tfidf_vectorizer.pkl', 'rb') as f1:
			self.embedding_foo = pickle.load(f1)

		with open('models/svm_model.pkl', 'rb') as f2:
			self.model_predict = pickle.load(f2)

		with open('database/categories.json', 'r', encoding='utf-8') as f:
			self.categories = json.load(f)['categories']

	def clean_text(self, senetence):
		word_lists = gensim.utils.simple_preprocess(senetence, min_len=3, max_len=7)
		clean_text = ' '.join(word_lists)
		return clean_text

	def tokenizer(self, text):
		return ViTokenizer.tokenize(text)
	
	def embedding(self, text_is_tokenized):
		embedding_vector =  self.embedding_foo.transform(text_is_tokenized)
		return embedding_vector
	
	def classify(self, sentence):
		clean_text = self.clean_text(sentence)
		token = self.tokenizer(clean_text)
		embedding_vector = self.embedding([token])
		res = self.model_predict.predict(embedding_vector)
		return self.categories[res[0]]
	

if __name__ == '__main__':
	classfier = classify_categories_by_name()
	res = classfier.classify('Kính lão đọc sách dành cho nữ phong cách thời trang đẹp mắt')
	print(res)