from django.shortcuts import render
import requests, os, json
from google.cloud import vision
from google.cloud.vision import types
import re

from .Post import Post
from .Influencer import Influencer


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_secrets.json'






#---------#---------#---------#---------#---------#--------#
def home(request):

	tags = []
	tag = []
	logos = []
	text = []
	instaDesc = []
	hashtags = []


	# returns URL's of most recent 20 (or 17) photos
	urls, instaDesc, hashtags, fullname, username = instaApiCall()
	results = googleApiCall(urls)

	bio = 'this is my bio'
	totalfollowers = 50
	maxlikes = 45


	"""
	print('\n')
	print('user: ' , username)
	print('full: ' , fullname)
	print('bio: ' , bio)
	print('totalfollowers: ' , totalfollowers)
	print('maxlikes: ' , maxlikes)
	print('\n')
	"""

	########################################################
	#
	# TO DO : Make this loop section better / more efficient
	#
	########################################################

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


	# Post
	#
	# url list
	# google logos list
	# google tags
	# google text
	# instagram caption 

	# Influencer
	# 
	# username
	# fullname
	# bio
	# posts - one post object
	# total followers
	# max likes from entire page 





	# Makes Post and Influencer objects
	postsList= []

	print('POST & INFLUENCER OBJECTS')

	for i in range(0,len(urls)):
		postsList.append(Post(urls[i], logos[i], tags[i], text[i], instaDesc[i]))


	for post in postsList : 
		print(post)
	
	influencerObject = Influencer(username,fullname,bio,postsList,totalfollowers,maxlikes)

	



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


	fullname = instaData['data'][0]['user']['full_name']
	username = instaData['data'][0]['user']['username']

	
	# gets 3 most recent pics 
	for x in range(3) :
		urls.append(instaData['data'][x]['images']['low_resolution']['url'])
	
		#print('url:' , instaData['data'][x]['images']['low_resolution']['url'])
		#print('like count:', instaData['data'][x]['likes']['count'] )
		#print('comment count:', instaData['data'][x]['comments']['count'] )
	
		if ((instaData['data'][x]['caption']) is not None) :
			#print('caption:' , instaData['data'][x]['caption']['text'])
			print('\n')
		else :
			#print('caption: none')
			#print('tags', instaData['data'][x]['tags'] )
			print('\n')
	
	
		if ((instaData['data'][x]['caption']) is not None) :
			instaDesc.append(instaData['data'][x]['caption']['text'])
			
			tempString=''.join(instaDesc[x])
			tags=re.findall(r"#(\w+)",tempString)
			hashtags.append(tags)
		else :
			instaDesc.append([])
			hashtags.append([])


	return urls, instaDesc, hashtags, fullname, username

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
	return render(request, 'bass/recommend.html', {'title': 'Recommend'})



