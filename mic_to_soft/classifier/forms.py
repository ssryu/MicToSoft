from django import forms
from .models import Classifier, Account, LearningModel

class ClassifierForm(forms.ModelForm):
    class Meta:
        model = Classifier
        fields = ['title', 'textdata']

class ClassifierAccount(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['ID', 'PASSWORD', 'Email']

class ClassifierModels(forms.ModelForm):
    class Meta:
        model = LearningModel
        fields = ['learningmodel', 'learningdata']
