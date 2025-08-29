# app.py
import streamlit as st
from Configs.DataIngestion import Loader
from Configs.TextSplitter import RecursiveCharacterTextSplitter
from Configs.LLM import build_index
#import streamlit as st
import tempfile
#from Configs.DataIngestion import Loader

st.title("Ask a question about the document")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt", "pptx"])
query = st.text_input("💡 Ask a question about the document")
if uploaded_file is not None:
    # Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    # Now pass the path to your Loader
        docs = Loader(temp_path)  

        st.write("✅ Document loaded successfully!")

    
        # 🔹 Chunking
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunked_docs = splitter.split_documents(docs)

        # 🔹 Build index
        index = build_index(chunked_docs)
        query_engine = index.as_query_engine()

        with st.spinner("🤖 Thinking..."):
            response = query_engine.query(query)

        st.subheader("✅ Answer")
        st.write(str(response))
