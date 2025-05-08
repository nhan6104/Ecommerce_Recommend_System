from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import chromadb
from config import API_KEY_GEMINI

class recommendSystem:
	def __init__(self):
		persistent_client = chromadb.PersistentClient(path="database/chroma_langchain_db")
		self.vector_store = Chroma(
			client=persistent_client,
			collection_name="ecommerce",
			embedding_function=GoogleGenerativeAIEmbeddings(
						model="models/text-embedding-004",
						google_api_key=API_KEY_GEMINI),
		)


	def add_documents(self, path, chunksize = 0, chunkoverlap = 0, separator="\n"):
		raw_documents = TextLoader(path).load()
		text_splitter = CharacterTextSplitter(chunk_size = chunksize, chunk_overlap = chunkoverlap, separator = separator)
		documnents = text_splitter.split_documents(raw_documents)
		self.vector_store.add_documents(documnents)


	def search(self, query = "Kính chống ánh sáng xanh", k = 20):
		return self.vector_store.similarity_search(query, k = k)
		
		 
		
if __name__ == '__main__':
	# items = pd.read_csv("fashion_accessories_2025_04_16.csv")
	# item = items.loc[items["_visible_impression_info_amplitude_category_l2_name"] == "Phụ kiện thời trang nam", "name"].reset_index(drop=True)[0]
	# print(item)
	rc = recommendSystem()
	# query = 'Gọng kính dành cho nữ'
	# data = rc.classify_categories.classify(query)
	# print(data)
	data = rc.search()
	print(data)
	data = rc.search(items=['Phụ kiện thời trang'])
	print(len(data))
	# res = list()
	# rc.add_documents('id_description.txt')
			

	# print((res))

