from django.db import models
from django.utils import timezone

class Account(models.Model):
    username = models.CharField(max_length = 100)
    password = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200)

    def __str__(self):
        return self.username

class Classifier(models.Model):
    userid = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500)
    learningdata = models.FileField(upload_to = 'textdata/')
    model = models.FileField(upload_to = 'model/')
    created_date = models.DateTimeField(default=timezone.now)

    # pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title
