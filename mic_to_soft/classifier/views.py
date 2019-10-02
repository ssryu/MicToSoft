from django.shortcuts import render, redirect

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Classifier
from .forms import ClassifierForm

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

def home(request):
    return render(request, 'classifier/home.html', {})

def about(request):
    return render(request, 'classifier/about.html', {})

def board(request):
    return render(request, 'classifier/board.html', {})

def mypage(request):
    return render(request, 'classifier/mypage.html', {})
