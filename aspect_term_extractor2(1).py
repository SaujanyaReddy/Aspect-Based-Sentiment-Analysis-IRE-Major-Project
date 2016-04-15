import pickle
import xml.sax


sentic=pickle.load(open('sentic_dump.p','rb'))
sentence=pickle.load(open('sentence_dump.p','rb'))
#polarity_dict=pickle.load(open('polarities.p','rb'))

point1 = ["VBD", "VB", "VBG", "VBN","VBP", "VBZ", "JJ", "JJR", "JJS", "RB", "RBR", "RBS"]
point2 = ["JJ", "JJR", "JJS", "RB", "RBR", "RBS"]
verb = ["VBD", "VB", "VBG", "VBN","VBP", "VBZ"]
noun = ["NN", "NNS", "NNP", "NNPS"]
adverb =["RB", "RBR", "RBS"]
adjective = ["JJ", "JJR", "JJS"]
auxiliary_verb = ["be" , "am" , "are", "is", "was", "being", "can", "could", "do", "did", "does", "doing", "have", "had",
         "has", "having", "may", "might", "might", "must", "shall", "should", "will", "'ve", "n't", "were"]
asdict={}
forpol=[]

def extractor(words = {}, sid=0):
	pol=[sid]
	aspect_terms=[]
        #has_auiliary = set(words.keys()).intersection(auxiliary_verb)
        has_auiliary = getAuxiliary(words)
        hasNsubj = findNsubj(words)
        if(hasNsubj):
            for word in words.keys():
                    if(not words[word].has_key("nsubj")):
                        continue
	        #if words[word].has_key("nsubj"):
                    #Point 1
                    if (words[word]["pos_tag"] in verb and checkModifiers(words, word)):
                        print "In 1"
                        print word
                        aspect_terms.append(word)
			pol.append(word)
                    
                        #Point 3
                    elif (not has_auiliary and words[word].has_key("dobj") and isNoun(words, words[word]["dobj"])):
                            if (not wordInSentic(words[word]["dobj"])):
                                print "In 3a"
                                print words[word]["dobj"]
                                aspect_terms.append(words[word]["dobj"])
				j = words[word]["dobj"]
				pol.append(j)
                            else:
                                print "In 3b"
                                print words[word]["dobj"]
                                aspect_terms.append(words[word]["dobj"])
				pol.append(words[word]["dobj"])
                                word1 = getNounConnectedByAny(words, words[word]["dobj"])
                                if (word1):
                                    print word1
                                    aspect_terms.append(word1)
				    pol.append(word1)
                        #point 2 
                        #elif (words[word]["pos_tag"] in verb) and getAdverbOrAdjective(words, word):
                    elif not has_auiliary and getAdverbOrAdjective(words, word) :
                            print "In 2"
                            if(words[word].has_key("nsubj") and not ("DT" in words[words[word]["nsubj"]]["pos_tag"])):
                                print words[word]["nsubj"] + " "
                                aspect_terms.append(words[word]["nsubj"])
				pol.append(words[word]["nsubj"])
                            #if(not ("DT" in words[word]["pos_tag"] or "PRP" in words[word]["pos_tag"])):
                            print word
                            aspect_terms.append(word)
			    pol.append(word)
                        #Point 4
                    elif not has_auiliary and (words[word].has_key("xcomp")):
                            print "In 4"
                            xcomp = words[word]["xcomp"]
                            word1 = getNounConnectedByAny(words, xcomp)
                            if(word1):
                                print word1
                                aspect_terms.append(word1)
				pol.append(word1)
                    #Point 5 & 6 & 7
                    elif(words[word].has_key("cop")):
                        dep = getDependency(words, word)
                        copv = words[word]["cop"]
                        if(wordInSentic(word) and words[word]["pos_tag"] in noun):
                            print "In 5"
                            print word
                            aspect_terms.append(word)
			    pol.append(word)
                        if(words[word].has_key("nsubj") and  not ("DT" in words[words[word]["nsubj"]]["pos_tag"] 
                            or "PRP" in words[words[word]["nsubj"]]["pos_tag"])):
                            print "In 6"
                            print words[word]["nsubj"]
                            aspect_terms.append(words[word]["nsubj"])
			    pol.append(words[word]["nsubj"])
                        if(dep):
                            print "In 7"
                            print dep
                            aspect_terms.append(dep)
			    pol.append(dep)

        else:
            print "In else"
            for word in words.keys():
                prepN = hasPropositionalNoun(words, word)
                tmp = getVmodorXcomp(words, word)
                if(tmp and wordInSentic(tmp)):
                    print "In 8"
                    print word
                    aspect_terms.append(word)
		    pol.append(word)
                elif(prepN):
                    print "In 9"
                    if(words[word].has_key("appos")):
                        print words[word]["appos"]
                        aspect_terms.append(words[word]["appos"])
			pol.append(words[word]["appos"])
                    #else:
                    #    print word
                    print prepN
                    aspect_terms.append(prepN)
		    pol.append(prepN)
                elif(words[word].has_key("dobj")):
                    print "In 10"
                    tmp1 = words[words[word]["dobj"]]["pos_tag"]
                    if( not (("DT" in tmp1) or ("PRP" in tmp1))):
                        print words[word]["dobj"]
                        aspect_terms.append(words[word]["dobj"])
			pol.append(words[word]["dobj"])
                 
        forpol.append(pol)
        pol=[]
    	return aspect_terms

'''
            #point 4
                elif (words[word]["pos_tag"] in verb) and (words[word].has_key("xcomp")):
                    cC = words[word]["xcomp"] #clausalComplement
                    if (isInOpinionlexicon(word)) and (isInOpinionlexicon(cC)):
                        prep = getProposition(words, cC)
                        if(prep and words[words[cC][prep]]["pos_tag"] in noun):
                            print words[cC][prep]
            #Point 5 & 6 & 7
                elif (words[word]["pos_tag"] in adjective) and words[word].has_key("cop"):
                    if(words[word].has_key("nsubj") and words[words[word]["nsubj"]]["pos_tag"] in noun):
                    #Point 6
                        if(not words[word].has_key("xcomp")):
                            print words[word]["nsubj"]
                    #Point 7
                        else:
                            print words[word]["xcomp"] + " " + word
	    else: 
                    #for word in words.keys():
            #Pont 8
                    prep = getProposition(words, word)
                    if (words[word]["pos_tag"] in point2) and words[word].has_key("xcomp"):
                        xcomp = words[word]["xcomp"]
                        if(words[xcomp]["pos_tag"] in verb):
                            print xcomp
            #Pont 9
                    elif prep and words[words[word][prep]]["pos_tag"] in noun:
                        print word
            #Point 10
            '''
def getVmodorXcomp(words={}, word=""):
    for key in words[word].keys():
        if((key == "vmod" or key == "xcomp")):
            tmp =  words[word][key]
            if(words[tmp]["pos_tag"] in (adverb or adjective)):
                return tmp
    return None

def hasPropositionalNoun(words={}, word=""):
    for key in words[word].keys():
        if ("prep" in key):
            tmp = words[word][key]
            if(words[tmp]["pos_tag"] in noun):
                return tmp
    return None

def getAuxiliary(words={}):
    for word in words.keys():
        for key in words[word]:
            if("aux" == key):
                return True
    return False

def getDependency(words={}, word=""):
    for key in words[word].keys():
        try:
            if(key != "xcomp"):
                continue
            tmp = words[word][key]
            if(words[tmp]["pos_tag"] in verb):
                return tmp
        except:
            continue
    return None

def findNsubj(words={}):
    for key in words.keys():
        if(words[key].has_key("nsubj")):
            return True
    return False

def checkModifiers(words = {}, word=""):
    try:
        tmp = words[word]["amod"]
        return wordInSentic(tmp)
    except:
        pass
    try:
        tmp = words[word]["advmod"]
        return wordInSentic(tmp)
    except:
        pass
    return False

def getProposition(words = {}, word=""):
    if (word=="" or len(words)==0):
        return None
    for i in words[word].keys():
        if "prep" in i:
            return i
    return None

def getAdverbOrAdjective(words = {}, word=""):
    for key in words[word].keys():
        tmp = words[word][key]
        try:
            if(key == "advmod"):
                return True
            elif(words[tmp]["pos_tag"] in (adverb + adjective)):
                return True
        except:
            continue
    return False

def getNounConnectedByAny(words={}, word=""):
    if (word=="" or len(words)==0):
        return None
    for dep in words[word].keys():	
        try:
	    if (words[words[word][dep]]["pos_tag"] in noun):
                return words[word][dep]
	except:
		continue

def isNoun(words={}, word=""):
    return (words[word]["pos_tag"] in noun)


def wordInSentic(word = ""):
    if word in sentic:
        return True
    else: # if: word in sentic xml 
        return False

def isInOpinionlexicon(word = ""):
	return wordInSentic(word)
    #return False
    #if word == "":
     #   return False
    #else: #if :word in opinion lexicon
     #   return True

def isNounSubject(words = {}):
    if (len(words) == 0):
	return None
    for word in words.keys():
	if words[word].has_key("nsubj"):
		print True, '0000000000000000000'
		return True
    return False
	
# def writeToXml():
# 	#f=open('result_final_v2.xml','r+')
# 	f=open('absa--test_totestOn.xml','r+')
# 	f1=open('result_final_x2_3.xml','w+')
# 	lines=f.readlines()
# 	towrite=""
# 	termPos={}
# 	for l in lines:
# 		newast=""
# 		#sid=""
# 		if "<sentence id" in l:
# 			print "HH:",l
# 			sid=l[15:len(l)-3]
# 			#print "SID::",sid
# 		if "<text>" in l:
# 			mylist=asdict[sid]
# 			for term in mylist:
# 				from_val=l.strip().find(term)-6
# 				termPos[term]='"'+str(from_val)+'"'+' to='+'"'+str(from_val+len(term))+'"'
# 				print term," ",termPos[term]
# 		if "<aspectTerms>" in l:
# 			newast+=l[0:22]
# 			#print sid
# 			if sid!="":
# 				aslist=asdict[sid]
# 				for term in aslist:
# 					pola=polarity_dict[sid][term]
# 					newast+="<aspectTerm term="+'"'+term+'"'+" polarity="+'"'+pola+'"'+" from="+termPos[term]+"/>\n"
# 				newast+=l[23:]
# 				towrite+=newast
# 				termPos={}
# 		else:
# 			towrite+=l;
# 	#print towrite
# 	f1.write(towrite)
# 	f1.close()

if __name__ == "__main__":
    #words = {}
#    words = {"word" : {"pos_tag" : "verb"},}	
    # Myaspect=extractor({u'and': {'pos_tag': u'CC'}, u'atmosphere': {'pos_tag': u'NN', u'advmod': u'pretty', u'det': u'a'}, u'it': {'pos_tag': u'PRP'}, u'an': {'pos_tag': u'DT'}, u'even': {'pos_tag': u'RB'}, u'$': {'pos_tag': u'$'}, u'service': {'pos_tag': u'NN', u'amod': u'excellent'}, u'make': {'pos_tag': u'VB', u'dobj': u'this', u'nsubj': u'food'}, u',': {'pos_tag': u','}, u'better': {'pos_tag': u'JJR', u'advmod': u'even'}, u'pretty': {'pos_tag': u'RB'}, u'!': {'pos_tag': u'.'}, u'5.99': {'pos_tag': u'CD'}, u'food': {'pos_tag': u'NN', u'conj_and': u'atmosphere', u'nn': u'Delicious'}, u'buffet': {'pos_tag': u'NN', u'dep': u'$', u'num': u'5.99', u'det': u'the', u'nn': u'lunch'}, u'choice': {'pos_tag': u'NN', u'prep_for': u'lunch', u'nsubj': u'it', u'det': u'an', u'amod': u'better'}, u'lunch': {'pos_tag': u'NN'}, u'excellent': {'pos_tag': u'JJ'}, u'a': {'pos_tag': u'DT'}, u'great': {'pos_tag': u'JJ'}, u'for': {'pos_tag': u'IN'}, u'this': {'pos_tag': u'DT', u'rcmod': u'makes'}, u'dinner': {'pos_tag': u'NN', u'conj_and': u'buffet'}, u'Delicious': {'pos_tag': u'NNP'}, u'the': {'pos_tag': u'DT'}, u'makes': {'pos_tag': u'VBZ', u'xcomp': u'choice', u'nsubj': u'choice'}},"1398")
    # print Myaspect
	for sid in sentence.keys():
    #get words as dictionary #graph
		print sid
            #subNoun = isNounSubject(sentence[sid])
		aspects=extractor(sentence[sid], sid)
		print "asp:",sid, " ",aspects
		asdict[sid]=aspects
#print forpol
	aspectdict=dict((x[0],(x[1:])) for x in forpol[0:])
	print "asd",asdict
	pickle.dump(aspectdict,open('aspect_dump.p','wb'))
	pickle.dump(asdict,open('aspect_dump_new.p','wb'))
