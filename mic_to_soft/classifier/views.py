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
from mic_to_soft.tasks import learn, classify

def index(request):
    # if request.method == 'POST':
    #     form = ClassifierForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/')

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
            json.dumps(
                {
                    'req' : str(request),
                    'data' : form,
                    'text' : result[0]
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
        model = str(classifier.train_data).replace('textdata', 'model')
        classifier.save()

        return JsonResponse(
            json.dumps({'result' : 'ok'}),
            status=200
            )

    return JsonResponse(
        json.dumps({'error' : 'something bad'}),
        status=400
        )

def board_models(request):
    classifiers = Classifier.objects.order_by("-pk")
    return render(request, 'classifier/board/models/models.html', {'classifiers' : classifiers})

def model_create(request):
    if request.method == 'POST':
        form = ClassifierForm(request.POST, request.FILES)
        if form.is_valid():
            classifier = form.save(commit=False)

            hash_value = str(classifier.id)
            hash_value = hashlib.sha256(hash_value.encode()).hexdigest()
            media_root = settings.MEDIA_ROOT
            train_data = 'textdata/' + str(classifier.train_data)

            classifier.model_hash = hash_value
            classifier.save()

            learn.delay(hash_value, media_root, train_data, model)

            return redirect('model_detail', pk=classifier.pk)
    else:
        form = ClassifierForm()
    return render(request, 'classifier/board/models/create.html', {'form' : form})

def model_detail(request, pk):
    classifier = get_object_or_404(Classifier, pk=pk)
    return render(request, 'classifier/board/models/detail.html', {'classifier': classifier})

def model_edit(request, pk):
    classifier = get_object_or_404(Classifier, pk=pk)
    passcheck = False
    print(classifier.password)
    if request.method == "POST":
        form = ClassifierEditForm(request.POST, request.FILES, instance=classifier)
        print(request.POST)

        if request.POST['original-password'] == classifier.password:
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
            passcheck = True

    else:
        form = ClassifierEditForm(instance=classifier)

    context = {
        'form': form,
        'passcheck':passcheck,
    }
    return render(request, 'classifier/board/models/edit.html', context)
