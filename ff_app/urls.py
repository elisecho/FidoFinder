from django.urls import include, path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'ff_app'
urlpatterns = [
    # ff Home Page
    path('', views.index, name='index'),

    # ff list of all owners
    path('pets', views.pets, name='pets'),

    # ff details a single owner and information about their pets
    path('pet/<int:pet_id>/', views.pet, name='pet'),

    # A form for users to register a new pet
    path('new_pet', views.new_pet, name='new_pet'),

    # A form for users to register a new harness
    path('new_harness/<int:pet_id>/', views.new_harness, name='new_harness'),

    # A form for users to edit an existing harness
    path('edit_harness/<int:harness_id>/', views.edit_harness, name='edit_harness'),
    #Bill's delete_harness code
    # A form for users to delete an existing harness
    path('delete_harness/<int:harness_id>/', views.delete_harness, name='delete_harness'),

    # A form for users to edit an existing pet
    path('edit_pet/<int:pet_id>/', views.edit_pet, name='edit_pet'),
    #Bill_Elise delete pet
    # A form for users to delete an existing pet
    path('delete_pet/<int:pet_id>/', views.delete_pet, name='delete_pet'),

    #change password page
    path('change_password/', views.change_password, name='change_password'),

    #successful password change notice
    path('success/', views.success, name='success'),
    
    #custom error page for when a user tries to access someone elses pet
    path('wrong_pet/', views.wrong_pet, name='wrong_pet'),
    
    #show owner's details
    path('owner_details/', views.owner_details, name='owner_details'),
    
    #edit owner's dtails
    path('edit_owner_details/', views.edit_owner_details, name='edit_owner_details'),
    
    #API for adding a pet's location
    path('locations/', views.LocationList.as_view()),
    
    #Random pet finder that uses the Petfinder API
    path('random_pet_finder/', views.random_pet_finder, name='random_pet_finder'),

    #Map path
    path('maps', include('maps.urls')),

]
