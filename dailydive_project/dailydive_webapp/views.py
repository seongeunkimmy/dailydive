from django.shortcuts import render

# Create your views here.

def home_view(request):
    return render(request, 'dailydive_webapp/home_view.html', {})