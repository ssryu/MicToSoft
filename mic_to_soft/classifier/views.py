from django.shortcuts import render, redirect

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Classifier
from .forms import ClassifierForm
from .forms import ClassifierAccount
from .forms import LearningModel

def index(request):
    if request.method == 'POST':
        form = ClassifierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'test' : 'test text'}

    datas = Classifier.objects.all()
    context['datas'] = datas

    form = ClassifierForm()
    context['form'] = form

    return render(request, 'classifier/index.html', context)

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
    if request.method == 'POST':
        form = ClassifierAccount(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ClassifierAccount()
    return render(request, 'classifier/sign/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = ClassifierAccount(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ClassifierAccount()

    return render(request, 'classifier/sign/signin.html', {'form': form})

def board(request):
    context = {'model1' : 'm1', 'data1' : 'd1'}

    return render(request, 'classifier/board/board.html', context)

def models(request):
    return render(request, 'classifier/board/models.html', {})

def newmodel(request):
    if request.method == 'POST':
        form = LearningModel(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = LearningModel()

    form = LearningModel()
    return render(request, 'classifier/mypage/newmodel.html', {'form' : form})

def data(request):
    return render(request, 'classifier/board/data.html', {})

def mypage(request):
    return render(request, 'classifier/mypage/mypage.html', {})

def account(request):
    form = ClassifierAccount()
    return render(request, 'classifier/mypage/account.html', {'form': form})

def managemodels(request):
    context = {'model1' : 'm1', 'data1' : 'd1'}

    return render(request, 'classifier/mypage/managemodels.html', context)

def about(request):
    return render(request, 'classifier/about/about.html', {})

def help(request):
    return render(request, 'classifier/about/help.html', {})
