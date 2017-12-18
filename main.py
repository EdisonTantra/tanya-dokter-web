import json
import os
from tfidf_search import run
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask_cors import CORS, cross_origin

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
		data = data = json.load(open('data/clean_data.json'))
		query1 = request.args.get('q1', '')
		query2 = request.args.get('q2', '')
		query3 = request.args.get('q3', '')
		max_response = request.args.get("max_resp", 10)

		queries = query1 + " " + query2 + " " + query3
		response = jsonify(run(data, queries, max_response))
		# response.headers.add('Access-Control-Allow-Origin', '*')
		return response

@app.route('/api/data/small', methods=['GET'])
def trainingData():
	data = json.load(open('data/training_data.json'))
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