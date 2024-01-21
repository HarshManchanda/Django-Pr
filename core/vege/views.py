from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse

#import user models for authentication
from django.contrib.auth.models import User

#To flash messages in django we have messages we can search on google by django message
from django.contrib import messages

#Inbuit django function for encryption of password
#Also, for session we use login method in django it helps in create session so next time it can recognize you 
#logout method is django inbuilt for logging out functionality
from django.contrib.auth import authenticate , login, logout

#Django decorator for authenticate recipes page only to user that login
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/login/")
def recipes(request):
    if request.method == "POST":
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')

        Recipe.objects.create(
            recipe_name = recipe_name,
            recipe_description = recipe_description,
            recipe_image = recipe_image
        )
        # print(recipe_name)
        # print(recipe_description)
        # print(recipe_image)

        return redirect('/recipes/')
    
    queryset = Recipe.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(recipe_name__icontains = request.GET.get('search'))

    context = {'recipes':queryset}

    return render(request, 'recipes.html', context)

def update_recipe(request,id):
    queryset = Recipe.objects.get(id=id)
    context = {'recipe':queryset}

    if request.method == "POST":
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')

        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description
        
        if recipe_image:
            queryset.recipe_image = recipe_image

        queryset.save()
        return redirect('/recipes/')

    return render(request, 'update_recipes.html', context)



def delete_recipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/recipes/')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.info(request, 'Invalid Username!')
            return redirect('/login/')
        
        user = authenticate(username = username, password = password)
        if user is None:
            messages.info(request, 'Invalid Password!')
            return redirect('/login/')
        
        else:
            login(request, user)
            return redirect('/recipes/')
                    
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')


def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, 'Username already taken!')
            return redirect('/register/')
    
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        #password must be in encrypt form as its in a string so we will use a specific method on user model

        user.set_password(password)
        user.save()
        messages.info(request, 'Account created Successfully!')
        return redirect('/register/')

    return render(request, 'register.html')