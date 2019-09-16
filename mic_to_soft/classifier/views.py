from django.shortcuts import render

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request, 'classifier/index.html', context = {'test' : 'test text'})

def index(request):
    return render(request, 'classifier/about.html', context = {'test' : 'test text'})

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
