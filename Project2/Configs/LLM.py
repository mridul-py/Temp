# Configs/LLMConfig.py
from llama_index.core import Settings, VectorStoreIndex
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

GoogleAPI="AIzaSyBhm7RE_cdi7IlXp2ovbwgXnWqTEJttaxs"

# LLM
llm = GoogleGenAI(model="gemini-2.5-flash", api_key=GoogleAPI)

# Embedding
embed_model = GoogleGenAIEmbedding(
    model_name="models/gemini-embedding-exp-03-07", 
    api_key=GoogleAPI
)

# Set globally
Settings.llm = llm
Settings.embed_model = embed_model

def build_index(docs):
    return VectorStoreIndex.from_documents(
        docs,
        llm=llm,
        embed_model=embed_model
    )
