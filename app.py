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


if __name__ == "__main__":
    app.run(debug=True)



