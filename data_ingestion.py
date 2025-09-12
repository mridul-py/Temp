from langchain_astradb import AstraDBVectorStore
# Import the new embedding model
from langchain_google_genai import GoogleGenerativeAIEmbeddings 
from dotenv import load_dotenv
import os
import pandas as pd
from echatbot.components.data_transformation import dataconveter

load_dotenv()

# Load the Google API key from the environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")

# Instantiate the GoogleGenerativeAIEmbeddings class
# The model name for embeddings is typically 'models/embedding-001'
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY
)

def ingestdata():
    vstore = AstraDBVectorStore(
        embedding=embedding,
        collection_name="chatbot_collection",
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )
    
    # Check if collection already has documents
    existing_docs = vstore.similarity_search("test", k=1)
    
    if not existing_docs:  # Only insert if collection is empty
        docs = dataconveter()
        inserted_ids = vstore.add_documents(docs)
        print(f"\nInserted {len(inserted_ids)} documents.")
        return vstore, inserted_ids
    else:
        print("\nDocuments already exist in the collection.")
        return vstore,None


if __name__ == '__main__':
    vstore, inserted_ids = ingestdata()
    #print(f"\nInserted {len(inserted_ids)} documents.")
    
    # The similarity search will now use the Google Gemini embeddings
    #results = vstore.similarity_search_with_score("Best in this price Bass 4.5*Sound 4.5*Battery backup 4.9*Design 4.2*",k=3)
   # for res ,score in results:
        #print(score)
        #print(res)
        #print(f"* {res.page_content} [{res.metadata}]")