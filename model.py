import os
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from utils import load_json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

school_data = load_json(os.path.join(BASE_DIR, "data", "school_data.json"))
training_data = load_json(os.path.join(BASE_DIR, "data", "training_data.json"))

questions = [item["question"] for item in training_data]
labels = [item["intent"] for item in training_data]

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(questions)

model = LogisticRegression(max_iter=200)
model.fit(X, labels)

embed_model = SentenceTransformer('all-MiniLM-L6-v2')
knowledge_texts = list(school_data.values())
knowledge_embeddings = embed_model.encode(knowledge_texts)

def semantic_search(user_input):
    user_embedding = embed_model.encode([user_input])
    similarity = cosine_similarity(user_embedding, knowledge_embeddings)
    best_match_index = np.argmax(similarity)
    return knowledge_texts[best_match_index]

def chatbot_response(user_input):
    if not user_input:
        return "Please enter a valid message."

    text = user_input.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    words = text.split()

    # ---- GREETINGS ----
    greeting_keywords = [
        "hi", "hii", "hiii", "hello", "hey",
        "good morning", "goodmorning", "gud mrng",
        "good afternoon", "goodafternoon",
        "good evening", "goodevening",
        "good day", "goodday", "gud day",
        "morning", "afternoon", "evening","greeting","greetings"
    ]

    if any(word in text for word in greeting_keywords):
        return "Good day! 👋 Welcome to the School AI Assistant. How may I assist you today?"


    # ---- THANK YOU ----
    thanks_keywords = ["thank", "thanks", "thankyou", "thx", "ty"]
    if any(word in text for word in thanks_keywords):
        return "You're most welcome! 😊 If you need anything else, feel free to ask."

    # ---- GOODBYE ----
    goodbye_keywords = ["bye", "goodbye", "see you", "exit", "quit"]
    if any(word in text for word in goodbye_keywords):
        return "Goodbye! 👋 Have a productive day ahead."

    try:
        user_vector = vectorizer.transform([user_input])
        probabilities = model.predict_proba(user_vector)
        confidence = np.max(probabilities)
        prediction = model.predict(user_vector)[0]

        if confidence >= 0.5:
            return school_data.get(prediction, "Information not available.")
        else:
            return semantic_search(user_input)

    except Exception as e:
        print("Model Error:", e)
        return "I'm having trouble understanding that. Please try again."
