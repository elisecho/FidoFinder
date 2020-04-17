from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.views import LogoutView, LoginView 
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
    '''Log out the user'''
    LogoutView(request)
    return HttpResponseRedirect(reverse('ff_app:index'))

def register(request):
    '''register a new user'''
    if request.method != 'POST':
        #display blank registration form.
        form = UserCreationForm()
    else:
        #process completed form.
        form = UserCreationForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            # log the user in and then redirect to home page.
            authenticated_user = authenticate(username=new_user.username,
                password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('ff_app:index'))
    
    context = {'form': form}
    return render(request, 'users/register.html', context)