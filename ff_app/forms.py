from django import forms
from .models import Pet, Harness

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'description']
        labels = {'name': 'Pet\'s name',
                  'description': 'Pet\'s description'
                 }

class HarnessForm(forms.ModelForm):
    class Meta:
        model = Harness
        fields = ['harnessID']
        labels = {'harnessID': 'Harness ID'}