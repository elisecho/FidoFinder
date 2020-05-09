from django.shortcuts import render

# Create your views here.
def default_map(request):
    return render(request, 'default.html', {})