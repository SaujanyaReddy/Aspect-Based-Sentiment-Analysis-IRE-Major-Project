import os
import sys
text=[]
#txt = open('Restaurants_Train_v2.xml', 'r')
txt = open('absa-test_new.xml', 'r')
sent=[]
for line in txt:
	if '<sentence id' in line:
		#print '\n'+line	
		#print "going to sent:",line
		line = line.strip()
		sent.append(line)
txt = open('absa-test_new.xml', 'r')

for line in txt:
	if '<text>' in line:
		#print line
		line = line.replace('</text>', '')
		line = line.replace('<text>','')
		line = line.replace('pound', 'kilo')
		line = line.replace('#','')
		#print "going to text::",line
		line=line.strip()
		text.append(line)

