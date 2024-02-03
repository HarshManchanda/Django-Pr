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

#Djanog Paginator for pagination
from django.core.paginator import Paginator

#Django Q -> Use for filter in search for student. It helps in or statement so that we can implement multiple search query.
from django.db.models import Q, Sum

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

def get_student(request):
    queryset = Student.objects.all()

    if request.GET.get('search'):
        search = request.GET.get('search')
        queryset = queryset.filter(
            Q(student_name__icontains = search) |
            Q(student_id__student_id__icontains = search) |
            Q(department__department__icontains = search) |
            Q(student_email__icontains = search) |
            Q(student_age__icontains = search)
        )


    paginator = Paginator(queryset, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)

    # print(page_obj.object_list)

    return render(request, 'report/students.html', {'queryset': page_obj})

from .seed import generate_report_card

def see_marks(request, student_id):
    # generate_report_card() 
    # Above Function is present in seed.py we use to for generating rank data. 
    
    queryset = SubjectMarks.objects.filter(student__student_id__student_id = student_id)
    total_marks = queryset.aggregate(total_marks = Sum('marks'))
    
    return render(request, 'report/see_marks.html', {'queryset':queryset, 'total_marks' : total_marks})
