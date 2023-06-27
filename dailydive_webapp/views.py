from django.shortcuts import render, redirect

# Create your views here.

def index(request):
      if request.method == "GET":
        redirect('')
      return render(request, "dailydive_webapp/home_view.html")

def home_view(request):
    return render(request, 'dailydive_webapp/home_view.html', {})

def add_diary(request):
    return render(request, 'dailydive_webapp/add_diary.html', {})

def activity(request):
    return render(request, 'dailydive_webapp/activity.html', {})