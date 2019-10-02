from django import forms
from .models import Classifier

class ClassifierForm(forms.ModelForm):
    class Meta:
        model = Classifier
        fields = ['title', 'textdata']
