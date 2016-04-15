import pickle
import a
import sys
sentic=pickle.load(open('sentic_dump.p','rb'))			#sentnic dictionary
sentence=pickle.load(open('sentence_dump.p','rb'))		#parser output dictionary
sentword=pickle.load(open('sentiword_dump.p','rb'))		#sentiwordnet dictionary
aspect=pickle.load(open('aspect_dump_new.p', 'rb'))			#aspect_term extractor dictionary
adav=["JJ", "JJR", "JJS", "RB", "RBR", "RBS"]
nnegative = ['not', 'Not', "n't"]
noun = ["NN", "NNS", "NNP", "NNPS"]
positive =1
negative = -1
neutral=0
polarity_dict={}
#print sentence.keys()

print 'askeys::',aspect.keys()
def extractor(words = {}, sid=0):				#sid = sentence id, and words = aspect terms 
	inner={}
	print words
	for j in words:						# one by one aspect terms theeskuntam
	    lit=[]
	    print j						#j is the aspect term
	    flag=0
	    print sid,j
	    p =  sentence[sid][j]				#parser lo nunchi aa aspect term theeskuntam, from that sid
	#    print p
	    if sentence[sid][j]['pos_tag'] in noun:		#then if aspect term is noun go inside
		#print 'yipppeeeeeee'
		for i in p:					#iterate through its values
		    if i != 'pos_tag':				#if key is not 'pos_tag' go inside
			#print p[i]
			#ptag = sentence[sid][p[i]]['pos_tag'] 	#
		
		        
			if wordInSentic(p[i]):			#aspect term tho relate aina each word sentnic lo unda choostham,
				flag=1				#based on that positive, negative, neutral values istham
#print i
				if float(sentic[p[i]])>0:	#each aspect term may have many words in relation, and each word,
					lit.append(positive)	#with differnt polarities, that's why store each polarity in a list=lit.
					#print 'positive'
				elif float(sentic[p[i]])<0:
					lit.append(negative)
					#print 'negative'
				else:
					lit.append(neutral)
					#print 'neutral'
			elif p[i] in nnegative:			#if the word is in negative list created above
				#print i
				flag=1
				lit.append(negative)
				#print 'negative'
			
			elif wordInsentiwordnet(p[i]):		#if the word in sentiwordnet in case not present in sentnic
				flag=1				
				#print i
				#print 'yes'
			#	print sentword[i]
				if sentword[p[i]] =='1':
					lit.append(positive)
				#	print 'positive'
				elif sentword[p[i]] == '0':
					lit.append(neutral)
				#	print 'neutral'
				else:
					lit.append(negative)
				#	print 'negative'
				
			if flag==0:				#if the words related to aspect not present in eitherof the above three,
				#print 'nope'			then search for the aspect term itself in the sentiment dictionaries
				if wordInSentic(j):
				    flag=1
				    if float(sentic[j])>0:
					lit.append(positive)
				#	print 'positive'
				    elif float(sentic[j])<0:
					lit.append(negative)
				#	print 'negative'
				    else:
					lit.append(neutral)
				#	print 'neutral'
				elif j in nnegative:
				    lit.append(negative)
				 #   print 'negative'
				elif wordInsentiwordnet(j):
		
				    if sentword[j] =='1':
					lit.append(positive)
				#	print 'positive'
				    elif sentword[j] == '0':
					lit.append(neutral)
				#	print 'neutral'
			 	    else:
					lit.append(negative)
				#	print 'negative'
			if flag == 0:					#finally even if the aspect term is unavailable give neutral tag
				lit.append(neutral)
				#print 'neutral'
	    #print '\n',lit,'\n'
	    k=0
	    #print 'coooooooooool'
	    #print lit
	    for i in lit:						#from above for each aspect may get many polarities, so		
		k=k+i							#averaging them here, and giving a final polarity.
	    #print k
	    if k >0:
		print 'positive'
		inner[j]='positive'
	    if k == 0:
		print 'neutral'
		inner[j]='neutral'
	    if k < 0:
		print 'negative'
		inner[j]='negative'
	print "sid:",sid
	polarity_dict[sid]=inner
def wordInsentiwordnet(i):

	if i in sentword:
	    return True
	else:
	    return False

def wordInSentic(word = ""):
    if word in sentic:
        return True
    else: # if: word in sentic xml 
        return False

if __name__ == "__main__":
    #words = {}
#    words = {"word" : {"pos_tag" : "verb"},}
	for sid in aspect.keys():				#aspect dictionary lo key sentence id and value aa sentence lo unna aspect terms
    #get words as dictionary #graph
		print sid
            #subNoun = isNounSubject(sentence[sid])
		extractor(aspect[sid], sid)			#one by one sentence id pampistam
	print polarity_dict
	pickle.dump(polarity_dict,open('polarities.p','wb'))

