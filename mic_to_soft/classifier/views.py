from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'classifier/index.html', context = {'test' : 'test text'})