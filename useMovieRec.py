import pymongo
import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()
# MongoDB connection

# Fetch the MongoDB password from the environment variable
mongo_password = os.getenv('MONGO_PASSWORD')

# Construct the MongoDB URI with the password
uri = f"mongodb+srv://gauravsingh13020:{mongo_password}@cluster0.987z9ny.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to the MongoDB cluster
client = pymongo.MongoClient(uri)

# Select the database and collection
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

query= "imaginary characters from outer space at war"

results = collection.aggregate([
    {"$vectorSearch": {
        "queryVector": generate_embedding(query),
        "path": "plot_embedding_hf",
        "numCandidates": 100,
        "limit": 4,
        "index": "PlotSemanticSearch"
    }}
]);

for documents in results:
    print(f'Movie Name: {documents["title"]},\nMovie Plot: {documents["plot"]},\nMovie Genres: {documents["genres"]}')