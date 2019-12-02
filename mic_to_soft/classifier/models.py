from django.db import models

class Classifier(models.Model):
    title = models.CharField(max_length = 200)

    textdata = models.FileField(upload_to = 'textdata/')

    # pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title

class Account(models.Model):
    ID = models.CharField(max_length = 100)
    PASSWORD = models.CharField(max_length = 200)
    Email = models.CharField(max_length = 200)

class LearningModel(models.Model):
    title = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500)
    learningdata = models.FileField()
    learningmodel = models.CharField(max_length = 100)
