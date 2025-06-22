from flask import Flask, render_template, request, jsonify
from webForms import *
import AmazonModel
import FlipkartModel

app = Flask(__name__)

@app.route('/')
def login():
	return render_template('login.html')


@app.route('/search')
def search():
	return render_template('search.html')


@app.route('/api/amazonFunction', methods=['GET'])
def amazon_function():
    search_term = request.args.get('searchTerm')
    amazon_data = AmazonModel.main(search_term)
	
    return amazon_data

@app.route('/api/flipkartFunction', methods=['GET'])
def flipkart_function():
    search_term = request.args.get('searchTerm')
    flipkartData = FlipkartModel.main(search_term)

    return flipkartData