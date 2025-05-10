# 🛍️ Tiki Product Classification & Recommendation Engine

This project demonstrates an end-to-end system for product classification and semantic recommendation using real data crawled from [Tiki.vn](https://tiki.vn).

## 🚀 Features
### 🛠️ Data Collection
##### a. `crawlProductInfo(category_name)`
- Sends a request to Tiki’s API to get product listings for a category.
- Creates a new SQLite table (e.g., `book_2025_04_20`) and inserts all product JSON fields as text.
- Category configurations (e.g., API params) are read from `menu.json`.

##### b. `crawlComment(table_name_product)`
- For each product in the given table, uses its `id`, `seller_id`, and `seller_product_id` to crawl review data.
- Creates a new table (same name) in the `estimate_product` database.
- Each review is saved as a row of serialized JSON.

### 🧪 ETL
- Crawled product data from **Tiki.vn** and stored it into SQLite3 database.
- Designed a full **ETL pipeline**:
  - **Extract from CSV**: Use `extract()` to load raw product data from a local `.csv` file into the SQLite database.
  - **Extract from SQLite**: Use loadDataFromTable() to retrieve and flatten data stored in SQLite after web crawling.
  - **Transform**: 
  - Flatten nested JSON objects.
  - Convert booleans (`"true"`, `"false"`) and nulls to standardized formats.
  - Fill missing values.
  - Use `loadDataToCSV(table_name)` to export clean, tabular data into a `.csv` file.

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
├── ETL/ # ETL pipeline: extract, transform, load
    ├── ETL.py             # ETL class implementation
    ├── CRUD.py            # CRUD operations for SQLite3
    ├── utils.py           # Helper function 
├── models/       # Store SVM model and TF-IDF model 
├── routes/       # Routes of app
├── services/ # TF-IDF + SVM training and prediction
    ├── classify.py           # E-commerce platforms for auto-tagging
    ├── ecommerceService.py   # Serivce for recommend system 
    ├── search.py             # Semantic search with embeddings 
├── database/ #ChromaDB database and sample datasets
└── README.md
```
## 📌 Requirements

- Python 3.10+
- API key for Google Generative AI (Gemini)
- Install dependencies:

```bash
pip install -r requirements.txt

```bash
python app.py
