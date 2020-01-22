# coding: UTF-8
from django.shortcuts import render, redirect, get_object_or_404

import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings

from .models import Classifier

from .forms import ClassifierForm
from .forms import ClassifierEditForm

# for generate hash of models
import hashlib
import datetime
from mic_to_soft.tasks import learn, classify

import requests

def index(request):
    return render(request, 'classifier/index.html')

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
            json.dumps( { 'class' : result } ),
            safe = False
        )

@csrf_exempt
def learning_finished(request):
    if request.method == "POST":
        form = request.POST
        acc = float(form['acc'])
        model_hash = form['model_hash']

        classifier = get_object_or_404(Classifier, model_hash = model_hash)
        classifier.acc_rate = acc
        classifier.model = str(classifier.train_data).replace('textdata', 'model')
        classifier.save()

        return JsonResponse(
            json.dumps( { 'result' : 'ok' } ),
            status=200,
            safe = False,
        )

    return JsonResponse(
        json.dumps( { 'error' : 'something bad' } ),
        status=400,
        safe = False,
    )

def board_models(request):
    classifiers = Classifier.objects.order_by("-pk")
    return render(request, 'classifier/board/models/models.html', {'classifiers' : classifiers})

def model_create(request):
    if request.method == 'POST':
        form = ClassifierForm(request.POST, request.FILES)
        if form.is_valid():
            classifier = form.save(commit=False)

            hash_value = classifier.userid + str(datetime.datetime.now())
            hash_value = hashlib.sha256(hash_value.encode()).hexdigest()
            media_root = settings.MEDIA_ROOT
            train_data = 'textdata/' + str(classifier.train_data)

            classifier.model_hash = hash_value
            classifier.save()

            classifier = get_object_or_404(Classifier, model_hash = hash_value)
            model = str(classifier.train_data).replace('textdata', 'model')

            learn.delay(hash_value, media_root, train_data, model)

            return redirect('model_detail', pk=classifier.pk)
    else:
        form = ClassifierForm()
    return render(request, 'classifier/board/models/create.html', {'form' : form})

def model_detail(request, pk):
    context = {}
    classifier = get_object_or_404(Classifier, pk=pk)
    context['classifier'] = classifier

    if request.method == "GET" \
    and request.GET.__contains__('sentence') \
    and request.GET['sentence'] != '' :
        # set parameter
        model = os.path.join(settings.MEDIA_ROOT, str(classifier.model))
        text = request.GET['sentence']
        # get result
        result_class = classify(model, text)
        context['classified'] = result_class

    return render(request, 'classifier/board/models/detail.html', context)

def model_edit(request, pk):
    classifier = get_object_or_404(Classifier, pk=pk)
    passcheck = False
    if request.method == "POST":
        form = ClassifierEditForm(request.POST, request.FILES, instance=classifier)

        if request.POST['entered-password'] == classifier.password:
            # done selected
            if request.POST.__contains__('done'):
                if form.is_valid():
                    classifier = form.save(commit=False)
                    classifier.modified_date = timezone.now()
                    classifier.save()
                    return redirect('model_detail', pk=classifier.pk)
            # delete selected
            elif request.POST.__contains__('delete'):
                Classifier.objects.filter(pk=pk).delete()
                return redirect('models')

        # password is wrong
        else:
            if request.POST.__contains__('models'):
                return redirect('models')
            passcheck = True
    else:
        form = ClassifierEditForm(instance=classifier)

    context = {
        'form': form,
        'passcheck':passcheck,
    }
    return render(request, 'classifier/board/models/edit.html', context)
