from django.shortcuts import render, redirect
from django.conf import settings

from . import inference_klue

from .utils import get_chart, get_bar_chart

import json
from django.http import JsonResponse

from .models import solutions
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import  method_decorator
#
# @method_decorator(csrf_exempt, name='dispath')


sentence = ''
# Create your views here.
def index(request):
    if request.method == "GET":
        redirect('')
    return render(request, "dailydive_webapp/home_view.html")

def home_view(request):
    return render(request, 'dailydive_webapp/home_view.html', {})

def add_diary(request):
    sentence = request.POST.get('target_sentence')
    request.session['sentence'] = sentence
    return render(request, 'dailydive_webapp/add_diary.html',  {})

def activity(request):
    questions = [
            {
                'id': 1,
                'question_text': '잠은 잘 잤어요?',
                'sub_question': '수면의 질',
                'answer_choices': [
                                {'answer':'아주 좋아요, 깊이 잘 잤어요.', 'score' : 10 }, 
                                {'answer': '보통이에요, 괜찮게 잤어요.', 'score' : 5}, 
                                {'answer': '안 좋아요, 푹 못 잤어요.', 'score' : 0}
                                ],
                'input_before': '오늘은',
                'input_after': '시간 정도 잤어요.',
            },
            {
                'id': 2,
                'question_text': '운동을 했나요? ',
                'sub_question': '운동 시간 및 강도',
                'input_before': '오늘은',
                'input_after': '분 정도 운동했어요.',
                'additional': '*고강도: 달리기, 크로스핏, 인터벌 트레이닝 / *적당한 강도: 빨리 걷기, 사이클링, 배드민턴',
                'answer_choices': [
                                {'answer':'고강도로 평소보다 숨이 훨씬 많이 찼어요.', 'score' : 10 }, 
                                {'answer': '적당한 강도로 평소보다 숨이 조금 더 찼어요.', 'score' : 7}, 
                                {'answer': '아니요, 오늘은 운동 안했어요.', 'score' : 0}
                                ],
            },
            {
                'id': 3,
                'question_text': '휴식을 취했나요?',
                'answer_choices': [
                                {'answer': '네, 충분히 쉬면서 하루를 보내 개운했어요.', 'score' : 20 }, 
                                {'answer': '적당히 쉬어서 컨디션이 괜찮아요.', 'score' : 15}, 
                                {'answer': '아니요, 바빠서 못 쉬었더니 많이 피곤하네요.', 'score' : 10}
                                ],
            },
            {
                'id': 4,
                'question_text': '식사는 잘 챙겨 먹었나요?',
                'answer_choices': [
                                {'answer': '네, 아침, 점심, 저녁을 모두 규칙적으로 먹었어요.', 'score' : 20 }, 
                                {'answer': '그런 편이에요, 두 끼를 챙겨 먹었어요.', 'score' : 15}, 
                                {'answer': '아니요, 밥 대신 간식으로 간단하게 떼웠어요.', 'score' : 10}
                                ],
            },
            {
                'id': 5,
                'question_text': '소셜미디어를 얼마나 썼나요?',
                'additional': '*소셜미디어: 카카오톡, 유튜브, 인스타그램처럼 사람들의 경험과 정보를 나누는 플랫폼',
                'answer_choices': [
                                {'answer': '전혀 열어보지 않았어요.', 'score' : 20 }, 
                                {'answer': '종종 열어봤고, 1시간 이내로 썼어요.', 'score' : 15}, 
                                {'answer': '자주 열어보고, 1시간 이상 썼어요.', 'score' : 10}
                                ],
            },
        ]
    
    if request.method == 'POST':
        data = json.loads(request.body)
        answers = data.get('answers', [])
        request.session['answers'] = answers

        response_data = {'message': 'Answers received successfully'}
        return JsonResponse(response_data)
    else:
        return render(request, 'dailydive_webapp/activity.html', {'questions': questions})


def solution(request):

        data = request.session.get('answers')
        data_int = [int(num) if num is not None else 0 for num in data]
        score = sum(data_int)
        act_chart = get_chart(data)

        target_sentence = request.session.get('sentence')
        model = settings.MODEL_KLUE
        tokenizer = settings.TOKENIZER_KLUE

        result, temp = inference_klue.predict_sentiment(target_sentence, tokenizer, model)
        chart = get_bar_chart(temp)
        obj = solutions.objects.filter(sentiment=result).values()
        context = {'target_sentence':target_sentence, 'result':result, 'score': score, 'chart':chart,'act_chart': act_chart, 'selected_db_1':obj[0], 'selected_db_2':obj[1], 'selected_db_3':obj[2]}
        return render(request, 'dailydive_webapp/solution.html', context)

