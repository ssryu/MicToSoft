from django.shortcuts import render

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request, 'classifier/index.html', context = {'test' : 'test text'})

@csrf_exempt
def api(request):
    if request.method == "POST":
        form = request.POST
        return JsonResponse(
            json.dumps(
                {
                    'req' : str(request),
                    'data' : form,
                    'text' : form['text'].split(" ")
                }
            ),
            safe = False
        )

def signup(request):
    return render(request, 'classifier/sign/signup.html', {})

def signin(request):
    return render(request, 'classifier/sign/signin.html', {})

def board(request):
    return render(request, 'classifier/board/board.html', {})

def models(request):
    return render(request, 'classifier/board/models.html', {})

def data(request):
    return render(request, 'classifier/board/data.html', {})

def mypage(request):
    return render(request, 'classifier/mypage/mypage.html', {})

def account(request):
    return render(request, 'classifier/mypage/account.html', {})

def managemodels(request):
    return render(request, 'classifier/mypage/managemodels.html', {})

def about(request):
    return render(request, 'classifier/about/about.html', {})

def help(request):
    return render(request, 'classifier/about/help.html', {})
