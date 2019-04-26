from django.shortcuts import render
import requests, os, json
from google.cloud import vision
from google.cloud.vision import types
import re

from .Post import Post
from .Influencer import Influencer
from .getInstaFollowers import Insta_Info_Scraper
from .getInstaFollowers import getMaxLikes

from .tf_idf_matching import Matching
from .Influencer_MongoDB import InfluencerDB

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_secrets.json'

#---------#---------#---------#---------#---------#--------#
def home(request):

	tags = []
	tag = []
	logos = []
	text = []
	instaDesc = []
	hashtags = []

	# Instagram API call
	urls, instaDesc, hashtags, fullname, username, profilepic = instaApiCall()
	results = googleApiCall(urls)
	instaUrl = 'https://www.instagram.com/' + username

	# InstaScrape
	instaData = {}
	engagementRatioDict = {}

	obj = Insta_Info_Scraper()
	obj.main(instaData, instaUrl)
	maxLikesDict,instaBioDict = getMaxLikes(instaData)

	maxlikes = int(maxLikesDict[username])
	totalfollowers = int(instaData[username])
	bio = instaBioDict[username]


	#---------#---------#---------#---------#---------#---------#
	# saves descriptions of labels from allTags
	# this is a list of lists
	for all_labels in results[0] :
		for eachPic in all_labels :
			tag.append(eachPic.description)
		logos.append(tag)
		tag = []

	# saves descriptions of logos from allTags
	# this is a list of lists
	for all_logos in results[1] :
		for eachPic in all_logos :
			tag.append(eachPic.description)
		tags.append(tag)
		tag = []

	# saves descriptions of text from allTags
	# this is a list of lists
	for all_text in results[2] :
		for eachPic in all_text :
			tag.append(eachPic.description)
		text.append(tag)
		tag = []

	#---------#---------#---------#---------#---------#---------#
	
	# Print post & influencer attributes
	print('\nPOST')
	print('url:' , urls)
	print('logos:' , logos)
	print('tags:' , tags)
	print('text:' , text)
	print('caption:' , instaDesc)
	
	print('\nINFLUENCER')
	print('username:' , username)
	print('fullname:' , fullname)
	print('bio:', bio)
	print('followers:' , instaData[username])
	print('maxlikes:', maxlikes)
	print('profile pic:' , profilepic)

	# Makes Post and Influencer objects
	postsList= []

	print('\nPOST & INFLUENCER OBJECTS')

	for i in range(0,len(urls)):
		postsList.append( Post( urls[i] , logos[i] , tags[i] , text[i] , instaDesc[i] ) )

	for post in postsList : 
		print(post)
		print('\n')

	influencerObject = Influencer( username , fullname , bio , postsList , totalfollowers , maxlikes , profilepic )
	#inf_db= InfluencerDB()
	#inf_db.addInfluencerToDB(influencerObject)

	#---------#---------#---------#---------#---------#---------#

	context = {
		'data': zip(urls, tags, logos, text, instaDesc, hashtags),
		'something': 'hey guys'
	}

	return render(request, 'bass/home.html', context ) 

#---------#---------#---------#---------#---------#--------#
def instaApiCall():
	
	r = requests.get("https://api.instagram.com/v1/users/self/media/recent/?access_token=12497873753.91017a2.fae49190455746d3b40c891a154d316d")
	instaData = r.json()
	
	


	urls = []
	instaDesc = []
	hashtags = []

	profilepic = instaData['data'][0]['user']['profile_picture']
	fullname = instaData['data'][0]['user']['full_name']
	username = instaData['data'][0]['user']['username']



	
	# gets 5 most recent pics 
	for x in range(5) :
		urls.append(instaData['data'][x]['images']['low_resolution']['url'])
	
		if ((instaData['data'][x]['caption']) is not None) :
			instaDesc.append(instaData['data'][x]['caption']['text'])
			tempString=''.join(instaDesc[x])
			tags=re.findall(r"#(\w+)",tempString)
			hashtags.append(tags)
		else :
			instaDesc.append([])
			hashtags.append([])

	return urls, instaDesc, hashtags, fullname, username, profilepic

#---------#---------#---------#---------#---------#--------
def googleApiCall(urls) :
	
	client = vision.ImageAnnotatorClient()
	image = vision.types.Image()

	logos_list = []
	labels_list = []
	text_list = []

	#gets tags for the urls
	for x in range(len(urls)) : 
		image.source.image_uri = urls[x]
		
		response = client.label_detection(image=image)
		labels = response.label_annotations
		labels_list.append(labels)

		response = client.text_detection(image=image)
		texts = response.text_annotations
		text_list.append(texts)

		response = client.logo_detection(image=image)
		logos = response.logo_annotations
		logos_list.append(logos)

	return logos_list, labels_list, text_list
	
#---------#---------#---------#---------#---------#--------#
def about(request):
	return render(request, 'bass/about.html', {'title': 'About'})

def recommend(request):

	return render(request, 'bass/recommend.html',{'title':'Recommend'})

def showResults(request):
	#companyName = request.GET.get('companyName')
	hashTags = request.GET.get('hashTags')
	#category = request.GET.get('category')
	minimumFollowers = request.GET.get('minFollowers')

	
	print(hashTags)
	
	print(minimumFollowers)

	match = Matching()
	match.parseCorpus_db()
	#print(match.query("fox harry trusted"))

	topList = match.query(hashTags)

	userName=[]
	name=[]
	bio=[]
	followers=[]
	userURL=[]
	profilePicList = []

	for i in topList:
		userName.append(i['username'])
		name.append(i['name'])
		bio.append(i['bio'])
		followers.append(i['total_followers'])

	for i in userName:
		urlLink='https://www.instagram.com/'+i+'/'
		userURL.append(urlLink)


	context = {
		'data': zip(userName,name,bio,followers,userURL),
		'something': 'hey guys'
	}
	return render(request, 'bass/showResults.html', context)
