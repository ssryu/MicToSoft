from django.db import models
from django.utils import timezone

class Classifier(models.Model):
    #userid = models.ForeignKey(Account, on_delete=models.CASCADE)

    userid = models.CharField(max_length = 32)
    password = models.CharField(max_length = 32)

    title = models.CharField(max_length = 32)
    description = models.CharField(max_length = 200)
    acc_rate = models.FloatField(blank=True, null=True)

    # traindata blank,null test:True -> deploy:false
    train_data = models.FileField(upload_to = 'textdata/')
    model = models.FileField(upload_to = 'model/', blank=True, null=True)
    model_hash = models.CharField(max_length=100, blank=True, null=False)

    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)
    # created_date = models.DateTimeField(default=timezone.now)
    # modified_date = models.DateTimeField(default=timezone.now, blank=True, null=True) # あとで修正

    # pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title
