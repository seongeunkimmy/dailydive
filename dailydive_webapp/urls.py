from django.urls import path
from . import views # 같은 폴더 내의 views.py를 import 

app_name = 'dailydive_webapp'

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('solution/', views.solution, name='solution'),
]