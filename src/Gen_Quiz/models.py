from django.db import models

# Create your models here.
class Quiz(models.Model):
    title = models.TextField()
    topic = models.TextField()
    noOfQuestions = models.TextField()

class Quiz2(models.Model):
    title1 = models.TextField()
    topic1 = models.TextField()
    noOfQuestions = models.TextField()