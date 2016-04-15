# Aspect-Based-Sentiment-Analysis-IRE-Major-Project

Additional Tools required:  
-- Stanford CoreNLP  
-- NLTK (WordNet)  

This repository contains all the codes required for Aspect Based Sentiment Analysis,  
a.py -> gets sentences from XML file inside <text></text> tag. Name the file you want to run on in a.py.  
1. First run corenlp.py which comes with Stanford CoreNLP Parser,  
2. Then in another terminal run client.py, replace the client.py of Stanford CoreNLP Parser with the one in this repo. It gives dictionaries, with sentences and there relations  
3. Run aspect_term_extracter.py  
4. Run pol.py. gives polarity of the aspect terms extracted from above step  
5. Run categorizer.py . Gives categories of the aspect terms.  
6. Run catpol.py. Gives polarity of the categories.  
7. Atlast run makeXML which creates an XML file with the sentences, aspect terms, polarities, categories and their polarities.  
