from __future__ import division
from sklearn.feature_extraction.text import TfidfVectorizer
from pprint import pprint
import operator
import string
import math
import json

def term_frequency(term, tokenized_document):
    return tokenized_document.count(term)

def sublinear_term_frequency(term, tokenized_document):
    count = tokenized_document.count(term)
    if count == 0:
        return 0
    return 1 + math.log(count)

def augmented_term_frequency(term, tokenized_document):
    max_count = max([term_frequency(t, tokenized_document) for t in tokenized_document])
    return (0.5 + ((0.5 * term_frequency(term, tokenized_document))/max_count))

def inverse_document_frequencies(tokenized_documents):
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, tokenized_documents)
        idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token)))
    return idf_values

def tfidf(documents):
    tokenized_documents = [tokenize(d) for d in documents]
    idf = inverse_document_frequencies(tokenized_documents)
    tfidf_documents = []
    for document in tokenized_documents:
        doc_tfidf = []
        for term in idf.keys():
            tf = sublinear_term_frequency(term, document)
            doc_tfidf.append(tf * idf[term])
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents

def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude    

tokenize = lambda doc: doc.lower().split(" ")

def run(data,queries, max_response = 10):

    # data = json.load(open('../preprocessing_data/clean_data.json'))

    # query1 = raw_input("Symptoms 1 : \n")
    # query2 = raw_input("Symptoms 2 : \n")
    # query3 = raw_input("Symptoms 3 : \n")
    # max_response = raw_input("Max response that you want : \n")

    # queries = query1 + " " + query2 + " " + query3

    all_documents = [queries]
    for entry in data:
        all_documents.append(entry["raw_data"])

    # data dari gejala 
    tfidf_doc = tfidf(all_documents)

    our_tfidf_comparisons = []
    score = {}

    for count_d, doc in enumerate(tfidf_doc):
        index = count_d - 1
        if index == -1:
            score["query"] = cosine_similarity(tfidf_doc[0], doc)
        else: 
            score[count_d] = cosine_similarity(tfidf_doc[0], doc)

    sorted_score = sorted(score.items(), key=operator.itemgetter(1), reverse=True)

    sorted_score = sorted_score[:int(max_response)+1]

    pprint(sorted_score)

    response = {}
    rank = 0
    for index,elem in sorted_score:
        if index != "query":
            data_index = index - 1
            response[rank] = data[data_index]

        rank += 1

    # pprint(response)

    with open('search_result.json', 'w') as outfile:
        json.dump(response, outfile)

    return response
    print("Your result in search_result.json")