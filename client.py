import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from pprint import pprint
import a
import pickle

class StanfordNLP:
    def __init__(self):
        self.server = ServerProxy(JsonRpc20(),
                                  TransportTcpIp(addr=("127.0.0.1", 8080),timeout=200.0))
    
    def parse(self, text):
        return json.loads(self.server.parse(text))
#ip = open('Restaurants_Train_v2_parsed.txt',)
i=0
sentence={}
print len(a.sent),len(a.text)
while i < len(a.sent):
	nlp = StanfordNLP()
	#print a.sent[i]
#	print a.text, i

	result = nlp.parse(a.text[i])
#pprint(result)
	words={}
	#pprint (result['sentences'][0]['dependencies'])
	#pprint (result['sentences'][0]['words'])
	for wl in result['sentences'][0]['words']:
		innerd={}
		#print wl[0],wl[1]['PartOfSpeech']
		innerd['pos_tag']=wl[1]['PartOfSpeech']
		for depl in result['sentences'][0]['dependencies']:
			if depl[1]==wl[0]:
				innerd[depl[0]]=depl[2]
			#	print depl[1],':',depl[2],'-->',depl[0]
		words[wl[0]]=innerd
	#print words
	print a.sent[i][14:len(a.sent[i])-2]
	sentence[a.sent[i][14:len(a.sent[i])-2]]=words
	i+=1
print "\n"
print sentence
pickle.dump(sentence,open('sentence_dump.p','wb'))
'''	result = nlp.parse(a.text[i])
	pprint(result)
#pprint (result['sentences'][0]['dependencies'])

	from nltk.tree import Tree
	tree = Tree.parse(result['sentences'][0]['parsetree'])
	pprint(tree)
	print '--------------------------------------\n--------------------------------------'
	i=i+1'''
