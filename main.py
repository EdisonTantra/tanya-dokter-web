import json
import os
from tfidf_search import run
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

app = Flask(__name__)

# def run(environ, start_response):
    
#     data = 'Hello, World!\n'
#     status = '200 OK'
#     response_headers = [
#         ('Content-type','text/plain'),
#         ('Content-Length', str(len(data)))
#     ]
#     start_response(status, response_headers)
#     return iter([data])

@app.route('/', methods=['GET'])
def main():
	error = None
	return render_template('index.html', error=error)

@app.route('/api/search/', methods=['GET'])
def search():
	if request.method == 'GET':
		data = data = json.load(open('data/training_data.json'))
		query1 = request.args.get('q1', '')
		query2 = request.args.get('q2', '')
		query3 = request.args.get('q3', '')
		max_response = request.args.get("max_resp", 10)

		queries = query1 + " " + query2 + " " + query3
		return jsonify(run(data, queries, max_response))

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