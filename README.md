# 🍳 FridgeSurvivalKit

*Because "random eggs + half an onion" should = dinner, not doom*

FridgeSurvivalKit is a **recipe hack generator** built especially for students who want to:

- 😎 Look like masterchefs  
- 🚫 Avoid another sad microwave meal  
- 💸 Use up those weird fridge leftovers  

## What's Cookin'?

- 🔍 **Random Ingredient Magic**  
  Got ketchup, stale bread, and 3 random veggies? We'll find a recipe that actually works.
  
- 🎓 **Dorm-Friendly Finds**  
  No fancy tools? No problem – these recipes work with just a microwave + a pinch of desperation.

## Screenshots

**Front Facing Page:**  
This is the home page where you enter your ingredients.  
![Front Facing Image](https://github.com/user-attachments/assets/7bd7ae8e-6513-4aca-82db-f261b0869344)

**Results Page:**  
After mixing up the ingredients, you'll see the recipe recommendations here.  
![Results Page Image](https://github.com/user-attachments/assets/4435130b-5d11-46da-a2f5-3691e2772baa)

## Installation

### Prerequisites

Make sure you have **Python 3.6+** installed. Then, install the required Python packages using pip:

```bash
pip install flask transformers torch numpy
```
Ensure that your project directory is like this: 
```
/Recommendation System
├── app.py               # Flask backend code
├── recipes.csv          # CSV file with recipe data (columns: ingredients, recipe, embedding)
└── templates
    └── index.html       # Front-end HTML file
```
## Running the Application
1. Clone the Repo
2. cd Recommendation System
3. Run the Flask App
```
python app.py
```
4. Open the application on http://127.0.0.1:5000/
   
## How It Works

**Input Ingredients:**  
Enter three ingredients you have on hand into the form.

**Mix It Up!:**  
Click the "Mix It Up!" button to send the ingredients to the backend.

**Recommendation Engine:**  
The backend uses DistilBERT to create an embedding from the combined ingredients and then calculates the cosine similarity with each pre-computed recipe embedding from the CSV file. The best matching recipes are returned as recommendations.

**Results Display:**  
The results page will display the recommended recipes along with their matching percentage and the list of ingredients used in each recipe.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to the developers behind [Flask](https://flask.palletsprojects.com/), [Transformers](https://huggingface.co/transformers/), and [DistilBERT](https://huggingface.co/distilbert-base-uncased).  
Inspired by the daily struggle of turning random leftovers into a satisfying meal.
