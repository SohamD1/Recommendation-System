import pandas as pd
from transformers import DistilBertTokenizer, DistilBertModel
import torch

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

data = pd.read_csv('recipes.csv')
data['embedding'] = data['ingredients'].apply(get_embedding)

def recommend_recipes(user_ingredients, data, top_n=3):
    user_embedding = get_embedding(user_ingredients)
    cos = torch.nn.CosineSimilarity(dim=1)
    data['similarity'] = data['embedding'].apply(lambda x: cos(user_embedding, x).item())
    recommendations = data.sort_values(by="similarity", ascending=False).head(top_n)
    return recommendations[["ingredients", "recipe", "similarity"]]

user_ingredients = input("Enter available ingredients (comma-separated): ")
results = recommend_recipes(user_ingredients, data)

print("\nRecommended Recipes:\n")
for _, row in results.iterrows():
    print(f"Ingredients: {row['ingredients']}")
    print(f"Recipe: {row['recipe']}")
    print(f"Similarity: {row['similarity']:.2f}\n")