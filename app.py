from flask import Flask, render_template, g, redirect, url_for, request, flash
import datetime
import requests
import json
from random import randint

app = Flask(__name__)

from secrets_api import API_ENDPOINT, API_KEY

@app.route('/')
def index():
    today = datetime.datetime.now().strftime("%A %d %B %Y")  # Sunday 18 March 2018
    return render_template('home.jinja2', today=today)


@app.route('/importer/<id>')
def importer(id):
    URL = API_ENDPOINT + "importer/" + id
    r = requests.get(URL, headers={"x-api-key": API_KEY})
    importer = json.loads(r.content)

    URL = API_ENDPOINT + "importer/" + id + "/products"
    r = requests.get(URL, headers={"x-api-key": API_KEY})
    importer_products = json.loads(r.content)

    URL = API_ENDPOINT + "importer/" + id + "/similar"
    r = requests.get(URL, headers={"x-api-key": API_KEY})
    similar_importers = json.loads(r.content)

    return render_template('importer.jinja2', importer=importer, importer_products=importer_products, similar_importers=similar_importers)


@app.route('/product/<id>')
def product(id):
    URL = API_ENDPOINT + "product/" + id
    r = requests.get(URL, headers={"x-api-key": API_KEY})
    product = json.loads(r.content)

    URL = API_ENDPOINT + "product/" + id + "/importers"
    r = requests.get(URL, headers={"x-api-key": API_KEY})
    product_importers = json.loads(r.content)

    return render_template('product.jinja2', product=product, product_importers=product_importers)


@app.route("/random")
def random():
    rdm = randint(1, 30529)
    return redirect(url_for("importer", id=rdm))


### search

import csv
import re

def fuzzyfinder(user_input, collection):
    suggestions = []
    pattern = '.*?'.join(user_input)  # Converts 'djm' to 'd.*?j.*?m'
    regex = re.compile(pattern, re.IGNORECASE)  # Compiles a regex.
    for item in collection:
        match = regex.search(item)  # Checks if the current item matches the regex.
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]


@app.route("/search/<q>")
def search(q):

    with open('static/data/products.csv', 'r') as f:
        reader = csv.reader(f)
        output_list = list(reader)
        name_to_id = dict((v,k) for k,v in dict(output_list).items())
        collection = [i[1] for i in output_list]
    
        ordered_matches = fuzzyfinder(q, collection)
        hits_products = [{"id": name_to_id[name], "name":name, "class":"product"} for name in ordered_matches]

    with open('static/data/importers.csv', 'r') as f:
        reader = csv.reader(f)
        output_list = list(reader)
        name_to_id = dict((v,k) for k,v in dict(output_list).items())
        collection = [i[1] for i in output_list]
    
        ordered_matches = fuzzyfinder(q, collection)
        hits_importers = [{"id": name_to_id[name], "name":name, "class":"importer"} for name in ordered_matches]
    
    return render_template('search.jinja2', hits_products=hits_products, hits_importers=hits_importers, q=q)





### dev graph

@app.route('/importer_graph/<id>')
def importer_graph(id):
    URL = API_ENDPOINT + "importer/" + id
    r = requests.get(URL, headers={"x-api-key": API_KEY})
    importer = json.loads(r.content)

    URL = API_ENDPOINT + "importer/" + id + "/products"
    r = requests.get(URL, headers={"x-api-key": API_KEY})
    importer_products = json.loads(r.content)

    URL = API_ENDPOINT + "importer/" + id + "/similar"
    r = requests.get(URL, headers={"x-api-key": API_KEY})
    similar_importers = json.loads(r.content)

    URL = API_ENDPOINT + "importer/" + id + "/similar/products"
    r = requests.get(URL, headers={"x-api-key": API_KEY})
    similar_importer_products = json.loads(r.content)

    return render_template('importer_graph.jinja2', importer=importer, importer_products=importer_products, similar_importers=similar_importers, similar_importer_products=similar_importer_products)



if __name__ == "__main__":
    app.run(debug=True)



