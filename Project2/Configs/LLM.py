from llama_index.vector_stores.astra import AstraDBVectorStore
#from llama_index.embeddings import GoogleEmbedding
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbeddings
from astrapy import DataAPIClient
#from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
#from llama_index.embeddings import GooglePalmEmbeddings

# Initialize
google_embeddings = GoogleGenAIEmbeddings()

# --- LLM + Embedding ---
GoogleAPI="AIzaSyBhm7RE_cdi7IlXp2ovbwgXnWqTEJttaxs"
llm = GoogleGenAI(model="gemini-2.5-flash", api_key=GoogleAPI)
embed_model = GoogleGenAIEmbeddings(model_name="models/embedding-001", api_key=GoogleAPI)



#GoogleAPI="AIzaSyBhm7RE_cdi7IlXp2ovbwgXnWqTEJttaxs"

def build_index(documents: list):
    #from astrapy.db import AstraDB, DataAPIClient  # Assuming you're using astrapy
    # You must also define or import your `embed_model` elsewhere

    # Initialize the client
    client = DataAPIClient("AstraCS:aiYgHyfyBKGwHFtDIOwNjbeR:5c87950ba4dc44028e165606abfd3aa614ad7b455a73c6a27dd4c7c8956cdd31")
    
    db = client.get_database_by_api_endpoint(
        "https://98d3458d-0b32-4a05-8150-968045be1cd0-us-east-2.apps.astra.datastax.com"
    )

    print(f"Connected to Astra DB: {db.list_collection_names()}")

    # Create collection (skip if already exists)
    if "my_docs2" not in db.list_collection_names():
        collection = db.create_collection(
            "my_docs2",
            definition={
                "vector": {
                    "dimension": 768,      # your embedding size
                    "metric": "cosine"     # cosine, euclidean, or dot_product
                }
            }
        )
        print(f"✅ Collection created: {collection.name}")
    else:
        print("Collection 'my_docs2' already exists.")

    # Get the collection
    col = db.get_collection("my_docs2")

    # Insert each document with its embedding
    for i, chunk in enumerate(documents):
        # Make sure `chunk` has "text" and "source"
        text = chunk.get("text")
        source = chunk.get("source", "")

        if not text:
            continue  # skip empty text

        # Generate embedding (requires embed_model to be defined)
        embedding = embed_model.get_text_embedding(text)

        # Insert into Astra
        col.insert_one({
            "_id": f"doc_{i}",
            "text": text,
            "source": source,
            "$vector": embedding
        })

    print("Inserted all chunks ✅")
    
def get_query_engine():
        # --- Astra Vector Store ---
    vector_store = AstraDBVectorStore(
        token="AstraCS:xpPNZzOCbZJANDmXcSSlZewu:7cef1a63eda22eb7d81d4b3a08aac04263563c30fcb42a997f7794778ba7d4f4",
        api_endpoint="https://8302d19c-062b-4309-b8b3-e87678056aff-us-east-2.apps.astra.datastax.com",
        keyspace="default_keyspace",
        collection_name="my_docs2",
        embedding_dimension=768  # must match your embedding model
    )

    # --- Retriever ---
    retriever = VectorIndexRetriever(
        vector_store=vector_store,
        embed_model=embed_model,
        similarity_top_k=5
    )

    # --- Query engine ---
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        llm=llm
    )
    return query_engine
