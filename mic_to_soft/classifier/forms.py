from django import forms
from .models import Classifier

class ClassifierForm(forms.ModelForm):
    class Meta:
        model = Classifier
        fields = ['userid', 'password', 'title', 'description', 'train_data']

class ClassifierEditForm(forms.ModelForm):
    class Meta:
        model = Classifier
        fields = ['userid', 'title', 'description', 'train_data']
