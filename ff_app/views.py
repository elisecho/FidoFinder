from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from .models import Pet, Harness, Location, Owner
from .forms import PetForm, HarnessForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LocationSerializer
from django.template.context_processors import request
import petpy, requests, json

# Create your views here.

def index(request):
    '''Finding Fido Home Page'''
    return render(request, 'ff_app/index.html')


@login_required
def pets(request):
    '''Show pets that belong to the logged in user'''
    pets = Pet.objects.filter(owner=request.user).order_by('date_added')
    context = {'pets': pets}
    return render(request, 'ff_app/pets.html', context)


@login_required
def pet(request, pet_id):
    '''Show a single pet and associated information'''
    pet = Pet.objects.get(id=pet_id)

    # Validate the pet belongs to the logged in user before returning data
    if pet.owner != request.user:
        return render(request, 'ff_app/wrong_pet.html')

    harnesses = pet.harness_set.order_by('-date_added')
    context = {'pet': pet, 'harnesses': harnesses}
    return render(request, 'ff_app/pet.html', context)

@login_required
def wrong_pet(request):
    '''custom error page for when someone is being naughty'''
    return render(request, 'ff_app/wrong_pet.html')


@login_required
def new_pet(request):
    '''register a new pet'''
    if request.method != 'POST':
        # No data was submitted; create a blank form.
        form = PetForm()
    else:
        # POST data was submitted, process the data.
        form = PetForm(request.POST)
        if form.is_valid():
            new_pet = form.save(commit=False)
            new_pet.owner = request.user
            new_pet.save()
            return HttpResponseRedirect(reverse('ff_app:pets'))

    context = {'form': form}
    return render(request, 'ff_app/new_pet.html', context)


@login_required
def new_harness(request, pet_id):
    '''register a new harness for a particular pet'''
    pet = Pet.objects.get(id=pet_id)

    if request.method != 'POST':
        # No data was submitted; create a blank form.
        form = HarnessForm()
    else:
        # POST data was submitted, process the data.
        form = HarnessForm(data=request.POST)
        if form.is_valid():
            new_harness = form.save(commit=False)
            new_harness.pet = pet
            new_harness.save()
            return HttpResponseRedirect(reverse('ff_app:pet', args=[pet_id]))

    context = {'pet': pet, 'form': form}
    return render(request, 'ff_app/new_harness.html', context)


@login_required
def edit_harness(request, harness_id):
    '''edit an existing harness'''
    harness = Harness.objects.get(id=harness_id)
    pet = harness.pet

    #validate requesting user is the pet's owner before making the change.
    if pet.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current harness information
        form = HarnessForm(instance=harness)
    else:
        # POST data submitted; process the data.
        form = HarnessForm(instance=harness, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ff_app:pet', args=[pet.id]))

    context = {'harness': harness, 'pet': pet, 'form': form}
    return render(request, 'ff_app/edit_harness.html', context)

@login_required
def edit_pet(request, pet_id):
    '''edit an existing pet'''
    pet = Pet.objects.get(id=pet_id)

    #validate requesting user is the pet's owner before making the change.
    if pet.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current harness information
        form = PetForm(instance=pet)
    else:
        # POST data submitted; process the data.
        form = PetForm(instance=pet, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ff_app:pet', args=[pet.id]))

    context = {'pet': pet, 'form': form}
    return render(request, 'ff_app/edit_pet.html', context)

@login_required
def change_password(request):
    '''view for users to change their password, using a standard PasswordChangeForm
    located in django.contrib.auth.forms library, NOT in the forms.py script'''
    if request.method != 'POST':
        form = PasswordChangeForm(request.user)
    else:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect(reverse('ff_app:success'))
    return render(request, 'ff_app/change_password.html', {'form': form})

def success(request):
    '''successful password change notification'''
    return render(request, 'ff_app/success.html')
#Bill's delete_harness code
@login_required
def delete_harness(request, harness_id):
    '''delete an existing harness'''
    harness = Harness.objects.get(id=harness_id)
    pet = harness.pet

    #validate requesting user is the pet's owner before making the change.
    if pet.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current harness information
        form = HarnessForm(instance=harness)
    else:
        # POST data submitted; process the data.
        form = HarnessForm(instance=harness, data=request.POST)
        if form.is_valid():
            harness.delete()
            return HttpResponseRedirect(reverse('ff_app:pet', args=[pet.id]))

    context = {'harness': harness, 'pet': pet, 'form': form}
    return render(request, 'ff_app/delete_harness.html', context)

@login_required
def delete_pet(request, pet_id):
    '''delete an existing pet'''
    pet = Pet.objects.get(id=pet_id)

    #validate requesting user is the pet's owner before making the change.
    if pet.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current harness information
        form = PetForm(instance=pet)
    else:
        # POST data submitted; process the data.
        form = PetForm(instance=pet, data=request.POST)
        if form.is_valid():
            pet.delete()
            return HttpResponseRedirect(reverse('ff_app:pets'))

    context = {'pet': pet, 'form': form}
    return render(request, 'ff_app/delete_pet.html', context)

@login_required
def owner_details(request):
    '''Show the the details of the logged in user'''
    owner = Owner.objects.filter(user=request.user)
    context = {'owner': owner}
    return render(request, 'ff_app/owner_details.html', context)

@login_required
def edit_owner_details(request, owner_id):
    '''edit the owner's details'''
    owner = Owner.objects.get(id=owner_id)

    #validate requesting user is the is correct before making the change.
    if owner.user != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current harness information
        form = OwnerForm(instance=owner)
    else:
        # POST data submitted; process the data.
        form = OwnerForm(instance=owner, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ff_app:owner_details', args=[owner.id]))

    context = {'owner': owner, 'form': form}
    return render(request, 'ff_app/edit_owner_details.html', context)

# API Functionality follows
class LocationList(APIView):
    
    # used to get all the locations in the database
    def get(self, request):
        locations1= Location.objects.all()
        serializer=LocationSerializer(locations1, many=True)
        return Response(serializer.data)
    
    # used to add a location to the database
    def post(self, request):
         serializer=LocationSerializer(data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Petfinder API
def random_pet_finder(request):
    #Establish authentication with Petfinder's API using our API key and Secret they provided us and assigning the token to a
    #variable "pf"
    pf = petpy.Petfinder(key="cSsIbBmTYRT3LOwOccdgcIoec9iLmZCfqTnWylxDD7R2BLFnwo", secret="AxwDvPFnx68TIeKYyT44wcKzxAe4B0nT5XiCV39F")
    #Pull a list of dog breeds from Petfinder's API and refortmat the output from json to a String.
    dog_breeds = str(pf.breeds('dog'))
    #strip json characters from the beginning of the string
    dog_breeds = dog_breeds.strip("{'breeds': {'dog': [")
    #strip json characters from the end of the string
    dog_breeds = dog_breeds.rstrip("]}}")
    #Pull a list of cat breeds from Petfinder's API and refortmat the output from json to a String.        
    cat_breeds = str(pf.breeds('cat'))
    #strip json characters from the beginning of the string    
    cat_breeds = cat_breeds.strip("{'breeds': {'cat': [")
    #strip json characters from the end of the string    
    cat_breeds = cat_breeds.rstrip("]}}")    
    context = {'dog_breeds': dog_breeds, 'cat_breeds': cat_breeds}
    return render(request, 'ff_app/random_pet_finder.html', context)


