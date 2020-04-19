from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from .models import Pet, Harness
from .forms import PetForm, HarnessForm

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
        raise Http404
    
    harnesses = pet.harness_set.order_by('-date_added')
    context = {'pet': pet, 'harnesses': harnesses}
    return render(request, 'ff_app/pet.html', context)


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
            

            