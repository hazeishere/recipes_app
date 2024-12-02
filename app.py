import bs4, requests
from flask import Flask, url_for, request, render_template, redirect
from model import *
import random

app = Flask(__name__)

def display(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        soup = bs4.BeautifulSoup(response.text, 'lxml')

        # Extract title
        title = soup.find('h1', class_='title').text if soup.find('h1', class_='title') else "未命名的食譜"

        # Extract image
        cover = soup.find('div', class_='recipe-cover')
        img = cover.find('img')['src'] if cover and cover.find('img') else None

        # Extract servings
        servings = soup.find('div', class_='servings')
        num = servings.find('span', class_='num').text if servings and servings.find('span', class_='num') else "0"

        # Extract ingredients and groups
        details_group = soup.find('div', class_='ingredients-groups')
        ingredients_tag = details_group.find_all('ul', class_='ingredients') if details_group else []

        ingredient_list = [
            ingredient.text.strip() for ingredient in ingredients_tag[0].find_all('li', class_='ingredient')
        ] if ingredients_tag else []

        group1_name = group1_ingredients_list = group2_name = group2_ingredients_list = None
        group3_name = group3_ingredients_list = None

        # Add checks for additional groups
        group_names = soup.find_all('div', class_='group-name')
        for i, tag in enumerate(group_names[:3]):  # Limit to three groups
            ingredients = ingredients_tag[i + 1].find_all('li', class_='ingredient') if i + 1 < len(ingredients_tag) else []
            ingredients_list = [ingredient.text.strip() for ingredient in ingredients]

            if i == 0:
                group1_name, group1_ingredients_list = tag.text.strip(), ingredients_list
            elif i == 1:
                group2_name, group2_ingredients_list = tag.text.strip(), ingredients_list
            elif i == 2:
                group3_name, group3_ingredients_list = tag.text.strip(), ingredients_list

        # Extract steps
        howto = soup.find('div', class_='recipe-details-howto')
        steps = howto.find('ul', class_='recipe-details-steps').find_all('li', class_='recipe-details-step-item') if howto else []
        steps_data = [
            {
                "text": step.find('p', 'recipe-step-description-content').text.strip(),
                "img": step.find('a').get('href') if step.find('a') else None
            }
            for step in steps if step.find('p', 'recipe-step-description-content')
        ]

        return {
            'title': title, 'img': img, 'num': num, 'ingredient_list': ingredient_list, 'steps_data': steps_data,
            'group1_name': group1_name, 'group1_ingredients_list': group1_ingredients_list,
            'group2_name': group2_name, 'group2_ingredients_list': group2_ingredients_list,
            'group3_name': group3_name, 'group3_ingredients_list': group3_ingredients_list
        }

    except Exception as e:
        print(f"Error fetching recipe data: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

count = 0
@app.route('/fetch_url')
def fetch_url():
        global count
        count += 1
        return render_template('error.html', error_message="沒抽到驚喜ＱＱ", count=count), 400


@app.route('/rice')
def rice():
    url = get_dish("https://icook.tw/categories/46")
    data = display(url)
    if data:
        return render_template('rice.html', **data, url=url)
    else:
        return redirect(url_for('fetch_url'))  # Corrected redirection
    
@app.route('/noodle')
def noodle():
    url = get_dish("https://icook.tw/categories/360")
    data = display(url)
    if data:
        return render_template('rice.html', **data, url=url)
    else:
        return redirect(url_for('fetch_url'))
    
@app.route('/chicken')
def chicken():
    url = get_dish("https://icook.tw/categories/38")
    data = display(url)
    if data:
        return render_template('rice.html', **data, url=url)
    else:
        return redirect(url_for('fetch_url'))

@app.route('/beef')
def beef():
    url = get_dish("https://icook.tw/categories/39")
    data = display(url)
    if data:
        return render_template('rice.html', **data, url=url)
    else:
        return redirect(url_for('fetch_url'))

@app.route('/pork')
def pork():
    url = get_dish("https://icook.tw/categories/40")
    data = display(url)
    if data:
        return render_template('rice.html', **data, url=url)
    else:
        return redirect(url_for('fetch_url'))

@app.route('/egg')
def egg():
    url = get_dish("https://icook.tw/categories/301")
    data = display(url)
    if data:
        return render_template('rice.html', **data, url=url)
    else:
        return redirect(url_for('fetch_url'))

@app.route('/soup')
def soup():
    url = get_dish("https://icook.tw/categories/8")
    data = display(url)
    if data:
        return render_template('rice.html', **data, url=url)
    else:
        return redirect(url_for('fetch_url'))

@app.route('/sweet')
def sweet():
    url = get_dish("https://icook.tw/categories/57")
    data = display(url)
    if data:
        return render_template('rice.html', **data, url=url)
    else:
        return redirect(url_for('fetch_url'))
    
@app.route('/surprise_me')
def surprise():
    url = get_surprise()  
    data = display(url)
    if data:
        return render_template('rice.html', **data, url=url)
    else:
        return redirect(url_for('fetch_url'))

    
app.run(debug=True)