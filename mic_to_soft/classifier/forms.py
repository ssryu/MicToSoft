from django import forms
from .models import Classifier, Account

class ClassifierAccount(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'password', 'email']

class ClassifierForm(forms.ModelForm):
    class Meta:
        model = Classifier
        fields = ['userid', 'password', 'title', 'description', 'train_data']
