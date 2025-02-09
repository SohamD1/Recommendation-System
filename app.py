import pandas as pd
from transformers import DistilBertTokenizer, DistilBertModel
import torch
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS 

app = Flask(__name__)  


tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')


def get_embedding(text):
    """Compute the embedding of input text."""
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze(0)  


data = pd.read_csv('recipes.csv')

data['embedding'] = data['ingredients'].apply(lambda x: get_embedding(str(x)).tolist())


def recommend_recipes(user_ingredients, data, top_n=3):
    """Recommend recipes based on cosine similarity."""
    user_embedding = get_embedding(user_ingredients) 
    cos = torch.nn.CosineSimilarity(dim=0) 


    def calculate_similarity(embedding):

        recipe_embedding = torch.tensor(embedding)
        return cos(user_embedding, recipe_embedding).item()
    
    data['similarity'] = data['embedding'].apply(calculate_similarity)


    recommendations = data.sort_values(by="similarity", ascending=False).head(top_n)
    return recommendations[["ingredients", "recipe", "similarity"]]
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendation', methods=['POST'])
def recommendation():
    user_inputs = request.json.get('ingredients')
    if not user_inputs:
        return jsonify({"error": "No ingredients provided"}), 400
    
    results = recommend_recipes(user_inputs, data)
    return jsonify(results.to_dict(orient='records')) 

if __name__ == '__main__':
    app.run(debug=True)
