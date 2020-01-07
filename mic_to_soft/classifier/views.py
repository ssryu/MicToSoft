from django.shortcuts import render, redirect, get_object_or_404

import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings

from .models import Classifier
from .models import Account
from .forms import ClassifierForm
from .forms import ClassifierAccount

import hashlib
from mic_to_soft.tasks import learn, classify

def index(request):
    if request.method == 'POST':
        form = ClassifierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'test' : 'test text'}

    datas = Account.objects.all()

    context['datas'] = datas

    form = ClassifierForm()
    context['form'] = form

    return render(request, 'classifier/index.html', context)

@csrf_exempt
def api(request):
    if request.method == "POST":
        form = request.POST
        model_hash = form['model_hash']
        text = form['text']

        classifier = get_object_or_404(Classifier, model_hash = model_hash)
        media_root = settings.MEDIA_ROOT
        model = os.path.join(media_root, str(classifier.model))

        result = classify(model, text)

        return JsonResponse(
            json.dumps(
                {
                    'req' : str(request),
                    'data' : form,
                    'text' : result
                }
            ),
            safe = False
        )

@csrf_exempt
def learning_finished(request):
    if request.method == "POST":
        form = request.POST
        model_hash = form['model_hash']
        acc = float(form['acc'])

        classifier = get_object_or_404(Classifier, model_hash = model_hash)
        classifier.acc_rate = acc
        classifier.save()

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
    # context = {'posts' : [{'model' : 'm1', 'data' : 'd1'}, {'model' : 'm2', 'data' : 'd2'}]}
    classifiers = Classifier.objects.all()
    return render(request, 'classifier/board/board.html', context = {'classifiers' : classifiers})

def createmodel(request):
    if request.method == 'POST':
        form = ClassifierForm(request.POST, request.FILES)
        if form.is_valid():
            classifier = form.save(commit=False)

            hash_value = classifier.userid + classifier.title
            media_root = settings.MEDIA_ROOT
            train_data = 'textdata/' + str(classifier.train_data)
            model = train_data.replace('textdata', 'model')

            classifier.model_hash = hashlib.sha256(hash_value.encode()).hexdigest()
            classifier.model = model
            classifier.save()

            learn(hash_value, media_root, train_data, model)
            return redirect('modeldetail', pk=classifier.pk)
    else:
        form = ClassifierForm()
    return render(request, 'classifier/board/createmodel.html', {'form' : form})

def created(request, pk):
    classifier = get_object_or_404(Classifier, pk=pk)
    return render(request, 'classifier/board/created.html', {'classifier': classifier})

def modeldetail(request, pk):
    classifier = get_object_or_404(Classifier, pk=pk)
    return render(request, 'classifier/board/modeldetail.html', {'classifier': classifier})

def models(request):
    return render(request, 'classifier/board/models.html', {})

def newmodel(request):
    if request.method == 'POST':
        form = ClassifierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ClassifierForm()
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
