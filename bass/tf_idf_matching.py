
from nltk.tokenize import RegexpTokenizer
from nltk. corpus import stopwords
from nltk. stem. porter import PorterStemmer
import math
import heapq

from .Influencer_MongoDB import InfluencerDB 

DESIRED_NO_OF_RESULTS=3     #this determines how many search results you will get
tokenizer= RegexpTokenizer(r'[a-zA-Z]+')            #creating tokenizer useing provided code
allStopwords= set(stopwords.words('english' ))       #set of all english stopwords
filename ="./debate.txt" 

class Matching:

    def __init__(self):

        self.paragraphs_and_tokens={}                    #dictionary to store each paragraph's LIST of tokens
        self.paragraphs_and_tokens_sets={}               #dictionary to store each paragraph's SET of tokens
        self.allParagraphs= []                           #list of all non-empty paragraphs
        self.document_parsed =False
        self.allInfluencer= []
        
    def stemTokens(self, tokens):                     #takes in list of tokens and stems them

        stemmer = PorterStemmer()
                      
        for i in range(len(tokens)):            #iterating over each token and stemming it
            tokens[i]= stemmer.stem(tokens[i])
        return tokens


    def Tokenize(self, paragraph):    #takes in document, sends list of tokens - stopwords to stemTokens

        words= paragraph.split()                                                          #get individual words from each paragraph
        filtered_words= [word.lower() for word in words if word.lower() not in allStopwords]  #removed stopwords from the paragram and converted to lowercase
        tokens= tokenizer.tokenize(str(filtered_words))                               #obtaining tokens from paragraph

        return self.stemTokens(tokens)                                            #stemming all tokens in the LIST of tokens


    def gettf(self, term, document):  #returns tf of a term in a document

        if term.lower()!=term: #if term has uppercase letters, return -1
            return -1.0000

        count= document.count(term)
        
        if count==0:
            return 0
        else:
            return 1+math.log10(count)
        

    def getidf(self, term): #calculates idf of a term using a dictionary of tokens of each document

        if term.lower()!=term: #if term has uppercase letters, return -1
            return -1

        if self.document_parsed==False:
            parseCorpus_db()

        totalDocuments= len(self.allParagraphs) #No. of documents
        count=0
        for key, value in self.paragraphs_and_tokens_sets.items():   #iterating over set of tokens in each paragraph
            if term in value:                                   #if term is present in the set, increment counter
                count+=1

        if count==0:                                            #return -1 if count=0
            return -1.0000
            #count=1
            
        #print(term," appeared ",count," times")
        return math.log10(totalDocuments/count)                        #using given formula for calculating idf
       

    def gidf(self, term): #calculates idf of a term using a dictionary of tokens of each document

        #print("IDF of ",term)
        
        if term.lower()!=term: #if term has uppercase letters, return -1
            return -1

        if self.document_parsed==False:
            parseCorpus_db()
            
        totalDocuments= len(self.allParagraphs) #No. of documents
        count=0
        for key, value in self.paragraphs_and_tokens_sets.items():   #iterating over set of tokens in each paragraph
            if term in value:                                   #if term is present in the set, increment counter
                count+=1

        if count==0:                                            #return -1 if count=0
            count=1

        #print(self.allParagraphs)
        #print(totalDocuments)
        #print(totalDocuments/count)
        return math.log10(totalDocuments/count)         


    def getqvec(self, qstring):

        totalDocuments= len(self.allParagraphs) #No. of documents
        if self.document_parsed==False:
            parseCorpus_db()
            
        #if totalDocuments==0:  #if corpus hasn't been parsed yet, parse it
            #parseCorpus_file()

        string_vector_list = self.Tokenize(qstring)
        string_vector_dict = {}

        vector_magnitude =0
        temp=[]                     #stores list of non-normalized tf-idf values

        #print("length: ", 
        
        vector_magnitude =0
        for term in string_vector_list:
            idf= self.gidf(term)
            
            tf_idf=idf * self.gettf(term,string_vector_list)
            string_vector_dict[term]= tf_idf
            vector_magnitude+= tf_idf * tf_idf  #finding magnitude as summation of sqaures of tf-ids
            #print("Vector Magnitude: ", vector_magnitude)

        vector_magnitude= math.sqrt(vector_magnitude)  # sqrt of magnitude for normalising vector  
        
        for key in string_vector_dict:
            string_vector_dict[key]=string_vector_dict[key]/vector_magnitude
            
        return string_vector_dict


    def modified_getqvec(self, qstring):

        totalDocuments= len(self.allParagraphs) #No. of documents

        if self.document_parsed==False:
            parseCorpus_db()
            
        #if totalDocuments==0:  #if corpus hasn't been parsed yet, parse it
            #parseCorpus_file()

        string_vector_list = qstring
        string_vector_dict = {}

        vector_magnitude =0
        for term in set(string_vector_list):
            idf= self.gidf(term)
            
            tf_idf=idf * self.gettf(term,string_vector_list)
            string_vector_dict[term]= tf_idf
            vector_magnitude+= tf_idf * tf_idf  #finding magnitude as summation of sqaures of tf-ids
            #print("Vector Magnitude: ", vector_magnitude)

        vector_magnitude= math.sqrt(vector_magnitude)  # sqrt of magnitude for normalising vector  
        
        for key in string_vector_dict:
            string_vector_dict[key]=string_vector_dict[key]/vector_magnitude
            
        return string_vector_dict

        #value corresponding to each token = idf(token) * summation of tf values for each doc


    def query(self, qstring):

        string_vector_list = self.Tokenize(qstring)
        qstring = self.getqvec(qstring)  #obtaining tf-idf values of each stemmed token in qstring
        
        tf_idf_values_dict = {}
        for document in self.paragraphs_and_tokens:  #for each paragraph

            tf_idf_values_dict[document]= self.modified_getqvec(self.paragraphs_and_tokens[document])
       
        #documentNo, maxVal= findMaxCosine(tf_idf_values_dict, qstring)
        #if maxVal==0.0:
            #return "No Match\n",maxVal
        
        topCandidates= self.findMaxCosine(tf_idf_values_dict, qstring) #list of maxVal, documentNumber
        result=[]
        influencer_result=[]

        total_engagement_index=0
        for maxVal, docNumber in topCandidates:
            total_engagement_index+= maxVal

        #print(total_engagement_index)
        
        for maxVal, docNumber in topCandidates:

            weighted_engagement_index=0
            if total_engagement_index>0:

                #print(self.allInfluencer[docNumber]["engagement_index"])
                weighted_engagement_index = self.allInfluencer[docNumber]["engagement_index"] * maxVal / total_engagement_index
            
            #result.append((self.allParagraphs[docNumber], maxVal))

            #print(weighted_engagement_index)
            if weighted_engagement_index>0:
                influencer_result.append((self.allInfluencer[docNumber], weighted_engagement_index))

        return influencer_result #returns (Influencer, match score) tuples
        

    def asimilarity(self, a,b): #NOT USED               #finds the common set of keys in both dicts a, b and retuns the dot product
        commonKeys= set.intersection(set(a.keys()), set(b.keys()))  #finding set intersection of sets of keys

        cosineSimilarity=0
        for key in commonKeys:
            cosineSimilarity+= a[key]*b[key]    #finding dot product

        return cosineSimilarity

                   
    def findMaxCosine(self, tf_idf_values_dict, qstring):

        allCosineSimilarities=[]                #cosine similarites of query-document pairs

        qStringKeys= set(qstring.keys())
        
        for document in tf_idf_values_dict:     #for each document's list of tf_idf values

            similarity=0
            
            if tf_idf_values_dict[document]=={}:    #if document had none of the tokens then similarity=0
                allCosineSimilarities.append(0)
                continue

            for val in qStringKeys:
                if val in tf_idf_values_dict[document]:
                    similarity= similarity+ qstring[val]*tf_idf_values_dict[document][val]
            allCosineSimilarities.append(similarity) 

        scoresWithIndex= [[allCosineSimilarities[i],i] for i in range(len(allCosineSimilarities))] # x in allCosineSimilarities]
        #print(scoresWithIndex)

        if len(allCosineSimilarities)>DESIRED_NO_OF_RESULTS:
            result= heapq.nlargest(DESIRED_NO_OF_RESULTS, scoresWithIndex)

        else:
            result= scoresWithIndex
            
        return result

    def parseCorpus_file(self):  #first method that parses the debate.txt to create documents

        print("Parsing Corpus...")
        file = open(filename, "r", encoding='UTF-8' )

        i=0
        for paragraph in file:

            if paragraph=="\n":                     #ignoring empty paras
                continue

            self.allParagraphs.append(paragraph)         #appending to list of all paragraphs in corpus

            stemmed_tokenized_paragraph= self.Tokenize(paragraph)#obtaining the stemmed and tokenized paragraph
            self.paragraphs_and_tokens[i]= stemmed_tokenized_paragraph #dictionary of paragraph # and list tokens
            self.paragraphs_and_tokens_sets[i]= set(stemmed_tokenized_paragraph) #dict of paragraph # and set of tokens
            i+=1

        self.document_parsed= True
        return

    def parseCorpus_db(self, minFollowers):

        print("Parsing Corpus from db...")

        inf_db= InfluencerDB()
        allInfluencers = inf_db.allInfluencer_name_username_paragraph_engagement_index_bio_followers_profile_pic_url_minFollowers(minFollowers)
        i=0

        #print(allInfluencers)
        
        for influencer in allInfluencers:
            #print(influencer)
            paragraph= influencer['paragraph']
            #print(paragraph)
            self.allParagraphs.append(paragraph)         #appending to list of all paragraphs in corpus
            self.allInfluencer.append(influencer)
            
            stemmed_tokenized_paragraph= self.Tokenize(paragraph)#obtaining the stemmed and tokenized paragraph
            self.paragraphs_and_tokens[i]= stemmed_tokenized_paragraph #dictionary of paragraph # and list tokens
            self.paragraphs_and_tokens_sets[i]= set(stemmed_tokenized_paragraph) #dict of paragraph # and set of tokens
            i+=1

        self.document_parsed= True
        #print("self.allParagraphs",self.allParagraphs)
        
#match= Matching()
#match.parseCorpus_db(0)
#print(match.query("shoes nike sneakers"))
