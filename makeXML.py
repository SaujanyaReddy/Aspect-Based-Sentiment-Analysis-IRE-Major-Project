import pickle
asdict=pickle.load(open('aspect_dump_new.p','rb'))
polarity_dict=pickle.load(open('polarities.p','rb'))
cats_dict=pickle.load(open('cats_dump.p','rb'))
catpol=pickle.load(open('polcat.p','rb'))
print asdict

def writeToXml():
	#f=open('result_final_v2.xml','r+')
	f=open('absa--test.xml','r+')
	f1=open('result_final_x2_REST__.xml','w+')
	lines=f.readlines()
	towrite=""
	termPos={}
	for l in lines:	
		newast=""
		newcat=""
		#sid=""
		if "<sentence id" in l:
			print "HH:",l
			sid=l[15:len(l)-3]
			#print "SID::",sid
		if "<text>" in l:
			mylist=asdict[sid]
			for term in mylist:
				from_val=l.strip().find(term)-6
				termPos[term]='"'+str(from_val)+'"'+' to='+'"'+str(from_val+len(term))+'"'
				print term," ",termPos[term]
		if "<aspectTerms>" in l:
			newast+=l[0:22]
			#print sid
			if sid!="":
				aslist=asdict[sid]
				for term in aslist:
					pola=polarity_dict[sid][term]
					newast+="<aspectTerm term="+'"'+term+'"'+" polarity="+'"'+pola+'"'+" from="+termPos[term]+"/>\n"
				#newast+=l[23:]
				print "ns:",newast
				towrite+=newast+"</aspectTerms>"
				termPos={}
		if "<aspectCategories>" in l:
			newcat+=l[0:27]
			if sid!="" and sid in cats_dict.keys():
				catList=cats_dict[sid]
				for cat in catList:
					print catpol[sid]
					d1={}
					for k in catpol[sid].keys():
						if cat in catpol[sid][k].keys():
							d1[cat]=catpol[sid][k][cat]
					print d1
					#pola=catpol[sid][cat]
					if cat=='military_service':
						cat='service'
					if cat=='atmosphere':
						cat='ambience'
					# add polarity
					newcat+="<aspectCategory category="+'"'+cat+'"'+" polarity="+'"'+pola+'"'+"/>\n"
				newcat+=l[27:]
				towrite+=newcat+"</aspectCategories>"
		else:
			if "</aspectTerms>" not in l and "<aspectTerms>" not in l and "</aspectCategories>" not in l:
				towrite+=l;
	#print towrite
	f1.write(towrite)
	f1.close()

writeToXml()
