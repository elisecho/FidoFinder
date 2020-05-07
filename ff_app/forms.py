from django import forms
from .models import Pet, Harness, Owner

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'description', 'disabilities']
        labels = {'name': 'Pet\'s name',
                  'description': 'Pet\'s description',
                  'disabilities': 'Pet\'s disabilities'}

class HarnessForm(forms.ModelForm):
    class Meta:
        model = Harness
        fields = ['harnessID']
        labels = {'harnessID': 'Harness ID'}

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['first_name', 'last_name', 'address1', 'address2', 'city',
                  'state', 'zip', 'phone_number']
        labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'address1': 'Address 1',
                  'address2': 'Address 2', 'city': 'City', 'state': 'State', 'zip': 'ZIP Code',
                  'phone_number': 'Phone Number'}