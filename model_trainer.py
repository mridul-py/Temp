import os
from dotenv import load_dotenv
import google.generativeai as genai
from echatbot.components.data_ingestion import ingestdata

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
def generation(vstore):
    conversation_history = []  # memory buffer

    def ask_bot(user_query: str):
       
        retriever_results = vstore.similarity_search_with_score(user_query, k=25)

        
        context_text = "\n".join([
            f"Product: {doc.page_content} | Metadata: {doc.metadata} "
            for doc, score in retriever_results
        ])

       
        history_text = "\n".join([
            f"USER: {h['user']}\nBOT: {h['bot']}" for h in conversation_history[-5:]  # last 5 turns
        ])

        # Build full prompt
        prompt_text = f"""
Your ecommerce bot is an expert in product recommendations and customer queries.
It analyzes product titles and reviews to provide accurate and helpful responses.
Ensure your answers are relevant to the product context and refrain from straying off-topic.
Your responses should be concise and informative.

PAST CONVERSATION:
{history_text}

PRODUCTS FOUND:
{context_text}

QUESTION: {user_query}

YOUR ANSWER:
"""
        print("\n--- Prompt to Gemini ---\n")
        print(prompt_text)
        print("\n--- End of Prompt ---\n")

        # Call Gemini
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt_text)

        # Save this turn into memory
        conversation_history.append({"user": user_query, "bot": response.text})
        print(conversation_history)
        return response.text

    return ask_bot

if __name__ == '__main__':
    vstore, inserted_ids = ingestdata()
    bot = generation(vstore)

    # Interactive loop for user queries
    while True:
        query = input("\nAsk your product question (or type 'exit'): ")
        if query.lower() in ["exit", "quit"]:
            break
        answer = bot(query)
        print("\nAnswer:", answer)
