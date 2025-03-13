from django.http import HttpResponse
from django.shortcuts import render
def home(request):
   return render(request, 'home/index.html')
def signup(request):
    return render(request,'home/signup.html')
def signin(request):
    return render(request,'home/signin.html')
def about(request):
    return HttpResponse('About page')
def contact(request):
    return HttpResponse('Contact page')
