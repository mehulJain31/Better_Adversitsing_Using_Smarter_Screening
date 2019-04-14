from pymongo import MongoClient, errors
import pymongo
from bson.binary import Binary
import gridfs

from .Influencer import Influencer
from .Post import Post

class InfluencerDB:

    #client, db = CreateDB()
    #InfluencerTable= db["Influencer"]   #collection

    def __init__(self):

        Client_Link= 'mongodb://Admin:Admin@cluster0-shard-00-00-es5xr.gcp.mongodb.net:27017,cluster0-shard-00-01-es5xr.gcp.mongodb.net:27017,cluster0-shard-00-02-es5xr.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'
        InfluencerDB_DataBase_Name= 'BASS_div_test'
        InfluencerTable_Name = "Influencer"

        try:
            self.client = MongoClient(Client_Link)
            self.db = self.client[InfluencerDB_DataBase_Name]
            self.InfluencerTable = self.db[InfluencerTable_Name]                
            #self.InfluencerTable.create_index([("username", pymongo.TEXT)],name= 'search_index', default_language='english')
            self.InfluencerTable.create_index("username", unique= True)
            
            dbconnStatusJsonString = 'Connection Successful!'
            print(dbconnStatusJsonString)
        
        except Exception as e:
            dbconnStatusJsonString = 'Please check your connection: '+ str(e)
            print(dbconnStatusJsonString)
            print("InfluencerDB object could not be created!")

        #self.client = client
        #self.db= db
        
        
        #return client,db

    def addInfluencerToDB(self, influencer):

        influencerDict= influencer.CreateInfluencerDict()

        try:
            x = self.InfluencerTable.insert_one(influencerDict)
            return x #we can get the ID for this record using x.inserted_id
        
        except errors.DuplicateKeyError as e:

            print("Duplicate key error, this influencer already exists")
            print("\n\n\n",e)

        
    
    def printAllInfluencers_extended(self):  #print all data about each influencer

        for influencer in self.InfluencerTable.find():
            print(influencer,"\n")

    def printAllInfluencers_brief(self):     #print just usernames of all influencers

        for influencer in self.InfluencerTable.find({}, {"username":1}):
            print(influencer)

    def findInfluencerByQuery(self, query):  #find influencer by query-https://www.w3schools.com/python/python_mongodb_query.asp
        #prints and returns result of query
        result= self.InfluencerTable.find(query)
        
        for x in result:
            print(x)

        return result

    def allInfluencer_username_paragraph_engagement_index(self):

        query= {"username":1,"paragraph":1,"engagement_index":1}
        result= self.InfluencerTable.find({}, query)
        #for influencer in result:
            #print(influencer)

        return result

    def allInfluencer_name_username_paragraph_engagement_index_bio_followers(self):

        query= {"name":1,"username":1,"paragraph":1,"engagement_index":1, "bio":1, "total_followers":1 }
        result= self.InfluencerTable.find({}, query)
        return result

    def findInfluencerByUsername(self, username):

        query= {"username":username}
        return self.findInfluencerByQuery(query)
    

    def findInfluencerByTotal_followers(self, minFollowers): #unsorted
        #returns influencers that have greater than minFollowers
        
        query= {"total_followers": {"$gt":minFollowers}}
        return self.findInfluencerByQuery(self.InfluencerTable, query)


    def findInfluencerByTotal_followers_sorted(self, minFollowers):

        #sorted in descending order of total_followers

        query= {"total_followers": {"$gt":minFollowers}}
        influencers= self.InfluencerTable.find(query).sort("total_followers", -1)

        for x in influencers:
            print(x)

        return x

    def deleteInfluencerByQuery(self, query):

        self.InfluencerTable.delete_one(query)

    def deleteInfluencerByUsername(self, username):

        query= {"username":username}
        self.deleteInfluencerByQuery(self.InfluencerTable, query)

    def updateInfluencerPosts_givenUsername(self, InfluencerTable, username, additionalPosts):
        #don't forget to update the paragraph
        pass
        #https://www.w3schools.com/python/python_mongodb_update.asp

        
    def updateInfluencerMax_likes_givenUsername(self, InfluencerTable, username, newMax_likes):
        #don't forget to update the engagaement index too
        pass
        #https://www.w3schools.com/python/python_mongodb_update.asp

"""

idb= InfluencerDB()


p1= Post("image 1 url",["brand1", "brand2"], ["tag1", "tag2"], ["text1","\ntest2"], "super bowl motha fuckaahh")
p2= Post("image 2 url",["brand3", "brand4"], ["tag1.1", "tag2.1"], ["text1","\ntest2"], "super bowl motha fuckaahh")
inf= Influencer("Divyanshu","Neil Kumar","here's my bio Divyanshu",[p1,p2],10, 20)
inf2= Influencer("Micah","Micah Kumar","here's my bio Divyanshu",[p1,p2],10, 20)
inf3 = Influencer("Sakshi","Sakshi Kumar","here's my bio Divyanshu",[p1,p2],10, 20)

inf4= Influencer("Mehul","Mehul Kumar","here's my bio Divyanshu",[p1,p2],10, 20)
inf5= Influencer("Eric","Eric Kumar","here's my bio Divyanshu",[p1,p2],10, 20)
inf6 = Influencer("Div","Div Kumar","here's my bio Divyanshu",[p1,p2],10, 20)

idb.addInfluencerToDB(inf)
idb.addInfluencerToDB(inf2)
idb.addInfluencerToDB(inf3)
idb.addInfluencerToDB(inf4)
idb.addInfluencerToDB(inf5)
idb.addInfluencerToDB(inf6)


print("\n print all influencers  \n\n")
idb.printAllInfluencers_extended()
print("\n print all influencers  \n\n")
idb.printAllInfluencers_brief()
print("\n  username_paragraph_engagement_index  \n\n")
idb.allInfluencer_username_paragraph_engagement_index()

print("\n find by username  \n\n")
idb.findInfluencerByUsername( "Divyanshu")
"""
"""
findInfluencerByTotal_followers(InfluencerTable, 50)
findInfluencerByTotal_followers_sorted(InfluencerTable, 50)
deleteInfluencerByUsername(InfluencerTable, "sakshiInstaLol")


#firstRow= {"username":"test username", "name":"TestName", "bio":"TestBio", "posts":["post1","post2","post3"], "tags":"","total_followers":100, "max_likes":500}
tags: space separated GC recognized tags, hashtags, post description
calculate engagement_ratio = max_likes / total_followers
"""
"""
test1 = db.test1
test1_1 = {'author': 'Sakshi',
'course': 'Senior Design'}

#result = test1.insert(test)
fs= gridfs.GridFS(db)
a = fs.put(b"hello world")

print(db)
print(test1)
"""
