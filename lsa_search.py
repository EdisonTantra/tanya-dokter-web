from semanticpy.vector_space import VectorSpace
import operator

def run(data, queries, max_response = 10):
	all_documents = []
	for entry in data:
		all_documents.append(entry["raw_data"])

	vector_space = VectorSpace(all_documents)

	#Search for cat
	indexed_result = {}
	result = vector_space.search([queries])
	index = 0

	for entry in result:
		indexed_result[index] = entry
		index += 1

	sorted_resp = sorted(indexed_result.items(), key=operator.itemgetter(1), reverse=True)
	print sorted_resp

	response = {}
	rank = 1
	for entry in sorted_resp:
		data_index = entry[0]
		
		response[rank] = data[data_index]
		rank += 1

	return response