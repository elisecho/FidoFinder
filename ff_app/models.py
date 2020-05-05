from django.db import models
from django.contrib.auth.models import User

#test
# Data models/Classes for the finding fido application.

#Drop down list for pet disabilities
DISABILITIES = (
    ('blind','blind'),
    ('deaf','deaf'),
    ('blind and deaf','blind and deaf'),
    ('none','none'),
)

class Pet(models.Model):
    '''A model of a Pet'''
    name = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    disabilities = models.CharField(max_length=20, choices=DISABILITIES, default='none')
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    
    def __str__(self):
        '''return a string representing a pet''' 
        return self.name

class Harness(models.Model):
    '''A model of a Pet Harness'''
    pet = models.ForeignKey(Pet, on_delete = models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    harnessID = models.CharField(max_length=100, unique=True)

    def __str__(self):
        '''return a string representing a harness'''
        return self.harnessID
    
class Location(models.Model):
    '''A model referencing a pet's location'''
    harness = models.ForeignKey(Harness, on_delete = models.CASCADE)
    timeStamp = models.DateTimeField(auto_now_add=True)
    lat = models.IntegerField()
    long = models.IntegerField()
    
    def __str__(self):
        '''return a string representing a location'''
        return "harness: " + self.harness.harnessID + ", date/time: " + str(self.timeStamp) + ", lat: " + str(self.lat) + ", long: " + str(self.long)