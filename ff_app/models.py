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


#Drop down list for what State an Owner lives in
STATE = (
    ('None','None'),
    ('Alabama','Alabama'),
    ('Alaska','Alaska'),
    ('Arizona','Arizona'),
    ('Arkansas', 'Arkansas'),
    ('California', 'California'),
    ('Colorado', 'Colorado'),
    ('Connecticut', 'Connecticut'),
    ('Delaware', 'Delaware'),
    ('Florida', 'Florida'),
    ('Georgia', 'Georgia'),
    ('Hawaii', 'Hawaii'),
    ('Idaho', 'Idaho'),
    ('Illinois', 'Illinois'),
    ('Indiana', 'Indiana'),
    ('Iowa', 'Iowa'),
    ('Kansas', 'Kansas'),
    ('Kentucky', 'Kentucky'),
    ('Louisiana', 'Louisiana'),
    ('Maine', 'Maine'),
    ('Maryland', 'Maryland'),
    ('Massachusetts', 'Massachusetts'),
    ('Michigan', 'Michigan'),
    ('Minnesota', 'Minnesota'),
    ('Mississippi', 'Mississippi'),
    ('Missouri', 'Missouri'),
    ('Montana', 'Montana'),
    ('Nebraska', 'Nebraska'),
    ('Nevada', 'Nevada'),
    ('New Hampshire', 'New Hampshire'),
    ('New Jersey', 'New Jersey'),
    ('New Mexico', 'New Mexico'),
    ('New York', 'New York'),
    ('North Carolina', 'North Carolina'),
    ('North Dakota', 'North Dakota'),
    ('Ohio', 'Ohio'),
    ('Oklahoma', 'Oklahoma'),
    ('Oregon', 'Oregon'),
    ('Pennsylvania', 'Pennsylvania'),
    ('Rhode Island', 'Rhode Island'),
    ('South Carolina', 'South Carolina'),
    ('South Dakota', 'South Dakota'),
    ('Tennessee', 'Tennessee'),
    ('Texas', 'Texas'),
    ('Utah', 'Utah'),
    ('Vermont', 'Vermont'),
    ('Virginia', 'Virginia'),
    ('Washington', 'Washington'),
    ('West Virginia', 'West Virginia'),
    ('Wisconsin', 'Wisconsin'),
    ('Wyoming', 'Wyoming')
    
)

class Owner(models.Model):
    '''A model of a pet's owner'''
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    address1 = models.CharField(max_length=150, null=True, blank=True)
    address2 = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50, choices=STATE, default='none')
    zip = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    
    