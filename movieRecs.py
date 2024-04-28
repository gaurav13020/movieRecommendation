import pymongo
import requests
import json

# MongoDB connection

client = pymongo.MongoClient("mongodb+srv://gauravsingh13020:R5CswiSLPdOiTasA@cluster0.987z9ny.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.sample_mflix
collection = db.movies

hf_token = os.getenv("HF_TOKEN")
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

def generate_embedding(text: str) -> list[float]:

    response = requests.post(
        embedding_url, 
        headers={"Authorization": f"Bearer {hf_token}"}, 
        json={"inputs": text})
    
    if response.status_code != 200:
        raise ValueError(f"Request returned an error: {response.status_code} {response.text}")
    
    return response.json()

for doc in collection.find({'plot': {'$exists': True}}).limit(50):
    doc['plot_embedding_hf'] = generate_embedding(doc['plot'])
    collection.replace_one({'_id': doc['_id']}, doc)
                            
