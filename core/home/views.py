from django.shortcuts import render

#To import backend response 
from django.http import HttpResponse

# Create your views here. 

def home(requests):
    people = [
        {"name":"Harsh Manchanda", "Age":22},
        {"name":"Sparsh Khurana", "Age":23},
        {"name":"Anupam Sharma", "Age":16},
        {"name":"Mayank Shivam", "Age":15},
        {"name":"Rohan Solanki", "Age":21},
    ]
    vegetables = ["Potato","Tomato","Carrot"]
    # return HttpResponse("<h1> Hey I am a django server </h1>")
    return render(requests, "home/index.html", context={'page':'Django Tutorial 2023', "peoples":people, "vegetables":vegetables})

def about(requests):
    context = {'page':'About'}
    return render(requests, "home/about.html",context)

def contact(requests):
    context = {'page':'Contact'}
    return render(requests, "home/contact.html",context)

def success_page(requests):
    print("*"*10)
    return HttpResponse("<h1>Hey this is a success page</h1>")
