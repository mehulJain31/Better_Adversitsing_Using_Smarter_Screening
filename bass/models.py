from django.db import models

# Create your models here.

class Advertiser(models.Model):

    companyName= models.CharField(max_length=50)
    category= models.CharField(max_length=50)
    textArea=models.CharField(max_length=100)
    minFollowers=models.TextField(max_length=10)


    def getCompanyName(self):
        return self.companyName

    def getCategory(self):
        return self.category

    def getTextArea(self):
        return self.textArea

    def getMinFollowers(self):
        return self.minFollowers

    # def __init__(self,companyName,category,textArea,minFollowers):
    #     self.companyName=companyName
    #     self.category=category
    #     self.textArea=textArea
    #     self.minFollowers=minFollowers
    #


