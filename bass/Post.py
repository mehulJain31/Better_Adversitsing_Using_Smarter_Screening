
class Post:


    def __init__(self, image_url, google_logos, google_tags, google_text, instagram_post_caption):

        self.image_url= image_url           #string
        #google_logos     #list of strings
        #google_tags= google_tags       #list of strings
        #google_text= google_text       #list of strings ( some \n here and there)
        #instagram_post_caption= instagram_post_caption #string- post description obtained via instagram API
        self.postTag= self.generatePostTag(google_logos,google_tags,google_text,instagram_post_caption)


    def print1(self) :
        print('\nprinting', self.image_url)
        print('\nprinting', self.postTag)
        print('\n')

    def __str__(self):
        return self.image_url + " " +self.postTag

    def __repr__(self):

        return "Post Object\n" + "image_url: "+self.image_url + "\nPost Tag: " + self.postTag

    def generatePostTag(self,google_logos,google_tags,google_text,instagram_post_caption):   #combines all info obtained from GC into 1 paragraph

        logos= " ".join(google_logos)
        tags= " ".join(google_tags)

        temp= " ".join(google_text)
        text=""
        for char in temp:
            if char!="\n":
                text+=char 
        
        temp= instagram_post_caption
        post_caption= ""
        for char in temp:
            if char!="#":
                post_caption+= char

        result=  logos+" "+ tags+ " "+ text + " "+ post_caption
        return result
