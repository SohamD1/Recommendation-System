import csv
import ast
import numpy as np
import torch
from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModel

app = Flask(__name__)
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModel.from_pretrained("distilbert-base-uncased")

def get_embedding(text):
    """
    Generate a mean-pooled embedding for the input text using DistilBERT.
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state 
    attention_mask = inputs["attention_mask"]
    mask = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()

    masked_embeddings = embeddings * mask
    summed = torch.sum(masked_embeddings, dim=1)
    counts = torch.clamp(mask.sum(dim=1), min=1e-9) 
    mean_pooled = summed / counts

    return mean_pooled.detach().numpy()[0]

recipes = []
csv_filename = "recipes.csv"  

with open(csv_filename, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            embedding = ast.literal_eval(row["embedding"])
        except Exception as e:
            print("Error parsing embedding:", row["embedding"], e)
            continue

        recipes.append({
            "ingredients": row["ingredients"],
            "recipe": row["recipe"],
            "embedding": np.array(embedding)
        })

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recommendation", methods=["POST"])
def recommendation():
    data = request.get_json()
    if not data or "ingredients" not in data:
        return jsonify({"error": "No ingredients provided."}), 400
    ingredients_list = data["ingredients"]
    query_text = ", ".join(ingredients_list)
    query_embedding = get_embedding(query_text)
    results = []
    for recipe in recipes:
        sim = cosine_similarity(query_embedding, recipe["embedding"])
        results.append({
            "recipe": recipe["recipe"],
            "ingredients": recipe["ingredients"],
            "similarity": sim
        })
    results = sorted(results, key=lambda x: x["similarity"], reverse=True)
    top_results = results[:5]

    return jsonify(top_results)

if __name__ == "__main__":
    app.run(debug=True)
