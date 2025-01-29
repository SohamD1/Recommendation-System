import pandas as pd
from transformers import DistilBertTokenizer, DistilBertModel
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS  # Cross-Origin Resource Sharing

app = Flask(__name__)  # Creates instance of Flask app
CORS(app)

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)  # Kept the tensor format (no squeeze().numpy())

# Load dataset and compute embeddings for each recipe
data = pd.read_csv('recipes.csv')
data['embedding'] = data['ingredients'].apply(get_embedding)

def recommend_recipes(user_ingredients, data, top_n=3):
    user_embedding = get_embedding(user_ingredients)
    
    cos = torch.nn.CosineSimilarity(dim=1) 
    data['similarity'] = data['embedding'].apply(lambda x: cos(user_embedding, x).item())
    recommendations = data.sort_values(by="similarity", ascending=False).head(top_n)
    return recommendations[["ingredients", "recipe", "similarity"]]

@app.route('/recommendation', methods=['POST'])
def recommendation():
    user_inputs = request.json.get('ingredients')
    if not user_inputs:
        return jsonify({"error": "No ingredients provided"}), 400
    
    results = recommend_recipes(user_inputs, data)
    return jsonify(results.to_dict(orient='records'))  # Convert results to JSON

if __name__ == '__main__':
    app.run(debug=True)
