from bert_embedding import BertEmbedding

class BertEncoder(object):

	def __init__(self):
		print("hello")


	def get_bert_embedding(self, input_string):
		sentences = input_string.split('\n')
		bert_embedding = BertEmbedding()
		result = bert_embedding(sentences)
		return result