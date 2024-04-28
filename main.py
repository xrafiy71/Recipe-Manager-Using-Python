from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        ingredients TEXT,
                        instructions TEXT
                    )''')
    conn.commit()
    conn.close()

# Route to add a new recipe
@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    name = request.form['name']
    ingredients = request.form['ingredients']
    instructions = request.form['instructions']

    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO recipes (name, ingredients, instructions)
                      VALUES (?, ?, ?)''', (name, ingredients, instructions))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Route to display all recipes
@app.route('/')
def index():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM recipes''')
    recipes = cursor.fetchall()
    conn.close()

    return render_template('index.html', recipes=recipes)

# Route to delete a recipe
@app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM recipes WHERE id = ?''', (recipe_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
