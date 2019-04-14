#!/usr/bin/python
# https://www.promptcloud.com/blog/how-to-scrape-instagram-data-using-python/
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
from instaloader import Instaloader, Profile

class Insta_Info_Scraper():

    def getinfo(self, url,instaData):
        html = urllib.request.urlopen(url, context=self.ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all('meta', attrs={'property': 'og:description'
                             })
        text = data[0].get('content').split()
        user = '%s %s %s' % (text[-3], text[-2], text[-1])
        followers = text[0]
        following = text[2]
        posts = text[4]
        username = user.split('@')[1]
        
        if(username.endswith(')')):
            username = username[:-1]

        instaData[username]=followers

    def main(self, instaData,url2):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE
        self.getinfo(url2,instaData)

def getMaxLikes(instaData):

    maxLikesDict = {}
    instaBioDict = {}

    for profile_name in instaData.keys():

        PROFILE = profile_name # Insert profile name here
        L = Instaloader()

        # Obtain profile
        profile = Profile.from_username(L.context, PROFILE)
        maxLikes = max(profile.get_posts(), key=lambda x: x.likes)
        maxLikesDict[profile_name]=maxLikes.likes
        instaBioDict[profile_name]=profile.biography

    return maxLikesDict,instaBioDict



