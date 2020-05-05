from .models import Location

from rest_framework import serializers

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        # if you want to display certain fields from the Location class, use the following
        # format, otherwise use '__all__' to display all the fields
        # fields = ['harness', 'timeStamp', 'lat', 'long']
        fields = '__all__'