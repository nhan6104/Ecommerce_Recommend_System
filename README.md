# 🛍️ Tiki Product Classification & Recommendation Engine

This project demonstrates an end-to-end system for product classification and semantic recommendation using real data crawled from [Tiki.vn](https://tiki.vn).

## 🚀 Features

### 🧪 Data Collection & ETL
- Crawled product data from **Tiki.vn** using the `requests` library.
- Designed a full **ETL pipeline**:
  - **Extract**: Load raw data from **SQLite3**.
  - **Transform**: Normalize nested JSON, cleanse inconsistent types, handle nulls, and standardize text.
  - **Load**: Store structured data into a relational database (e.g., PostgreSQL).

### 🧠 Product Classification
- Transformed product names into feature vectors using **TF-IDF**.
- Trained a **Support Vector Machine (SVM)** classifier to predict product categories based on names.

### 🤖 Semantic Product Recommendation
- Generated high-quality text embeddings with **Google Gemini (text-embedding-004)**.
- Stored and retrieved similar products using **ChromaDB**, enabling fast and scalable vector search.
- Integrated **LangChain**:
  - Preprocessed product descriptions using `CharacterTextSplitter`.
  - Generated embeddings with `GoogleGenerativeAIEmbeddings`.
  - Enabled **semantic search** with natural language queries.

## 🛠️ Technologies Used

- Python, SQLite3, PostgreSQL
- `requests`, `scikit-learn`, `pandas`, `langchain`, `chromadb`
- Google Generative AI (Gemini Embeddings)
- SVM, TF-IDF, vector similarity search

## 📦 Use Cases

- Auto-classify product names into categories  
- Recommend similar or related products based on meaning, not just keywords  
- Enable natural language product search (e.g., "wireless mouse with silent clicks")

## 📂 Folder Structure
```
├── crawler/ # Scripts to crawl data from Tiki
├── etl/ # ETL pipeline: extract, transform, load
├── classifier/ # TF-IDF + SVM training and prediction
├── recommender/ # Semantic search with embeddings + ChromaDB
├── data/ # SQLite3 database and sample datasets
└── README.md
```
## 📌 Requirements

- Python 3.10+
- API key for Google Generative AI (Gemini)
- Install dependencies:

```bash
pip install -r requirements.txt
