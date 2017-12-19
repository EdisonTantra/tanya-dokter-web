import json
import os
import time
from tfidf_search import run as tfidf
from lsa_search import run as lsa
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask_cors import CORS, cross_origin
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
def main():
	error = None
	return render_template('index.html', error=error)

@app.route('/api/search/', methods=['GET'])
@cross_origin()
def search():
	if request.method == 'GET':
		data = data = json.load(open('data/training_data.json', encoding="utf-8"))
		algo = request.args.get('algo', '1')
		query1 = request.args.get('q1', '')
		query2 = request.args.get('q2', '')
		query3 = request.args.get('q3', '')
		max_response = request.args.get("max_resp", 10)
		start = time.time()
		print("timer start")

		queries = query1 + " " + query2 + " " + query3
		#remove stopwords
		factory = StopWordRemoverFactory()
		stopword = factory.create_stop_word_remover()
		stopword.remove(queries)

		#stemming
		factory = StemmerFactory()
		stemmer = factory.create_stemmer()
		queries = stemmer.stem(queries)

		if algo == '1':
			response = jsonify(tfidf(data, queries, max_response))
		else:
			response = jsonify(lsa(data, queries, max_response))
		end = time.time()
		print("timer stop. Runtime: ")
		print(end - start)
		return response

@app.route('/api/data/small', methods=['GET'])
def trainingData():
	data = json.load(open('data/training_data.json', encoding="utf-8"))
	return jsonify(data)

@app.route('/api/data/real', methods=['GET'])
def cleanData():
	data = json.load(open('data/clean_data.json'))
	return jsonify(data)	

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
	app.run(host='0.0.0.0')