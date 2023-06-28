from django.shortcuts import render, redirect
from django.conf import settings

from . import inference_klue
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import  method_decorator
#
# @method_decorator(csrf_exempt, name='dispath')


# Create your views here.
def index(request):
      if request.method == "GET":
        redirect('')
      return render(request, "dailydive_webapp/home_view.html")

def home_view(request):
    return render(request, 'dailydive_webapp/home_view.html', {})

def solution(request):
    return render(request, 'dailydive_webapp/solution.html', {})

def add_diary(request):
    return render(request, 'dailydive_webapp/add_diary.html', {})

def activity(request):
    return render(request, 'dailydive_webapp/activity.html', {})

def klue_predict(request):
    target_sentence = request.POST['target_sentence']
    model = settings.MODEL_KLUE
    tokenizer = settings.TOKENIZER_KLUE

    result, temp = inference_klue.predict_sentiment(target_sentence, tokenizer, model)
    context = {'target_sentence':target_sentence, 'result':result, 'temp':temp}
    return render(request, 'dailydive_webapp/klue_predict.html', context)



