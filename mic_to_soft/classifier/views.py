from django.shortcuts import render, redirect, get_object_or_404

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import Classifier

from .forms import ClassifierForm

# for generate hash of models
import hashlib

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
    classifiers = Classifier.objects.order_by("-pk")
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
            return redirect('model_detail', pk=classifier.pk)
    else:
        form = ClassifierForm()
    return render(request, 'classifier/board/models/create.html', {'form' : form})

def model_detail(request, pk):
    classifier = get_object_or_404(Classifier, pk=pk)
    return render(request, 'classifier/board/models/detail.html', {'classifier': classifier})

def model_edit(request, pk):
    classifier = get_object_or_404(Classifier, pk=pk)
    if request.method == "POST":
        form = ClassifierForm(request.POST, request.FILES, instance=classifier)
        if form.is_valid():
            classifier = form.save(commit=False)
            classifier.modified_date = timezone.now()
            classifier.save()

            return redirect('model_detail', pk=classifier.pk)
    else:
        form = ClassifierForm(instance=classifier)

    return render(request, 'classifier/board/models/edit.html', {'form': form})
