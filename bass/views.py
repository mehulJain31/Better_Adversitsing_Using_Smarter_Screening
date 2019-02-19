from django.shortcuts import render
import requests, os, json
from google.cloud import vision
from google.cloud.vision import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_secrets.json'


#---------#---------#---------#---------#---------#--------#
def home(request):

	tags = []
	tag = []
	logos = []

	# returns URL's of most recent 20 (or 17) photos
	urls = instaApiCall()
	results = googleApiCall(urls)
	
	# results[0] : labels / tags
	# results[1] : logos
	
	# saves descriptions of labels from allTags
	# this is a list of lists
	for all_labels in results[0] :
		for eachPic in all_labels :
			tag.append(eachPic.description)
		tags.append(tag)
		tag = []

	# saves descriptions of logos from allTags
	# this is a list of lists
	for all_logos in results[1] :
		for eachPic in all_logos :
			tag.append(eachPic.description)
		logos.append(tag)
		tag = []
	
	print('tags' , tags)
	print('logos' , logos)
	#test

	context = {
		'data': zip(urls,tags,logos),
		'something': 'hey guys'
	}
	
	return render(request, 'bass/home.html', context ) 

#---------#---------#---------#---------#---------#--------#
def instaApiCall():
	r = requests.get("https://api.instagram.com/v1/users/self/media/recent/?access_token=10707224361.97fec5c.93afb151e0c9499187c2794dbd9cdb29")
	instaData = r.json()
	
	urls = []

	#gets the 7 most recent photos
	for x in range(10) :
		urls.append(instaData['data'][x]['images']['low_resolution']['url'])

	return urls

#---------#---------#---------#---------#---------#--------#
def googleApiCall(urls) :
	
	client = vision.ImageAnnotatorClient()
	image = vision.types.Image()

	logos_list = []
	labels_list = []

	#gets tags for the urls
	for x in range(len(urls)) : 
		image.source.image_uri = urls[x]
		
		response = client.label_detection(image=image)
		labels = response.label_annotations
		labels_list.append(labels)

		response = client.logo_detection(image=image)
		logos = response.logo_annotations
		logos_list.append(logos)

		
	return logos_list, labels_list
	
#---------#---------#---------#---------#---------#--------#
def about(request):
	return render(request, 'bass/about.html', {'title': 'About'})




