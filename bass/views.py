from django.shortcuts import render
import requests, os, json
from google.cloud import vision
from google.cloud.vision import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_secrets.json'


#---------#---------#---------#---------#---------#--------#
def home(request):

	# returns URL's of most recent 20 (or 17) photos
	urls = instaApiCall()
	allTags = googleApiCall(urls)
	tags = []
	tag = []

	# saves descriptions from allTags
	# this is a list of lists (tags)
	for a in allTags :
		for b in a :
			tag.append(b.description)
		tags.append(tag)
		tag = []

	print('URL size: ' , len(urls))
	print('TAGS\n' , tags)

	context = {
		'data': zip(urls,tags),
		'something': 'hey guys'
	}
	
	return render(request, 'bass/home.html', context ) 

#---------#---------#---------#---------#---------#--------#
def instaApiCall():
	r = requests.get("https://api.instagram.com/v1/users/self/media/recent/?access_token=10707224361.97fec5c.93afb151e0c9499187c2794dbd9cdb29")
	instaData = r.json()
	
	urls = []

	#gets the 7 most recent photos
	for x in range(7) :
		urls.append(instaData['data'][x]['images']['low_resolution']['url'])

	return urls

#---------#---------#---------#---------#---------#--------#
def googleApiCall(urls) :
	
	client = vision.ImageAnnotatorClient()
	image = vision.types.Image()

	tags = []

	#gets tags for the urls
	for x in range(len(urls)) : 
		image.source.image_uri = urls[x]
		response = client.label_detection(image=image)
		labels = response.label_annotations
		tags.append(labels)

	return tags
	
#---------#---------#---------#---------#---------#--------#
def about(request):
	return render(request, 'bass/about.html', {'title': 'About'})


#---------#---------#---------#---------#---------#--------#
def _main() :
  instaApiCall()



#---------#
if __name__ == '__main__' :
  _main()

#---------#---------#---------#---------#---------#--------#



