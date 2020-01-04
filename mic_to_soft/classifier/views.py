from django.shortcuts import render, redirect, get_object_or_404

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import Classifier
from .models import Account
from .forms import ClassifierForm
from .forms import ClassifierAccount

# for generate hash of models
import hashlib

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

def board_models(request):
    classifiers = Classifier.objects.all()
    return render(request, 'classifier/board/models/models.html', {'classifiers' : classifiers})

def model_create(request):
    if request.method == 'POST':
        form = ClassifierForm(request.POST, request.FILES)
        if form.is_valid():
            classifier = form.save(commit=False)
            hash_value = str(classifier.id)
            classifier.model_hash = hashlib.sha256(hash_value.encode()).hexdigest()
            classifier.acc_rate = 98.7
            classifier.save()
            return redirect('detail', pk=classifier.pk)
    else:
        form = ClassifierForm()
    return render(request, 'classifier/board/models/create.html', {'form' : form})

def model_detail(request, pk):
    classifier = get_object_or_404(Classifier, pk=pk)
    return render(request, 'classifier/board/models/detail.html', {'classifier': classifier})
