from flask import Flask, render_template, request, redirect, url_for
import configparser
import requests

app = Flask(__name__)
app.debug = True

@app.route('/')
def main():
    data = get_categories()
    print(data)
    return render_template('index.html', data=data)

def get_categories():
    api_url = "https://www.themealdb.com/api/json/v1/1/categories.php"
    r = requests.get(api_url)
    return r.json()['categories']

@app.route('/recipes')
def get_recipes():
    category = request.args.get('c')
    if category is None:
        return redirect(url_for('main'))
    api_url = "https://www.themealdb.com/api/json/v1/1/filter.php?c=" + category
    r = requests.get(api_url)
    data = r.json()['meals']
    return render_template('recipes-menu.html', data=data, cat=category)

@app.route('/recipe')
def get_recipe_by_mealid():
    mealid = request.args.get('id')
    if mealid is None:
        return redirect(url_for('main'))
    api_url = "https://themealdb.com/api/json/v1/1/lookup.php?i=" + mealid
    r = requests.get(api_url)
    data = r.json()['meals'][0]
    print(data)
    return render_template('recipe.html', data=data)

@app.route('/search')
def search():
    query = request.args.get('q')
    if query is None:
        return redirect(url_for('main'))
    api_url = "https://www.themealdb.com/api/json/v1/1/search.php?s=" + query
    r = requests.get(api_url)
    data = r.json()['meals']
    return render_template('search-result.html', data=data, query=query)
    
if __name__ == '__main__':
    # print(get_categories())
	app.run()