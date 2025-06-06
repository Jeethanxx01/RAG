from langchain_astradb import AstraDBVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
from moviebot.data_converter import dataconverter

load_dotenv()

# Load environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")

# Initialize the embedding model
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY
)

def ingestdata(status):
    # Initialize AstraDB vector store
    vstore = AstraDBVectorStore(
        embedding=embedding,
        collection_name="moviebot",
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )
    
    storage = status
    
    if storage == None:
        # Convert and ingest data if no existing storage
        docs = dataconverter()
        inserted_ids = vstore.add_documents(docs)
    else:
        return vstore
    
    return vstore, inserted_ids

if __name__ == '__main__':
    # Test the ingestion
    vstore, inserted_ids = ingestdata(None)
    print(f"\nInserted {len(inserted_ids)} documents.")
    
    # Test a sample query
    results = vstore.similarity_search("Tell me about action movies with high ratings")
    for res in results:
        print(f"\nTitle: {res.metadata['title']}")
        print(f"Genre: {res.metadata['genre']}")
        print(f"Rating: {res.metadata['rating']}")
        print(f"Overview: {res.page_content}") 