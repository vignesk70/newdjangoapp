
# Create your models here.
from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin

# Create your models here.
class Question(models.Model):
    question_text=models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return f"The question is {self.question_text}"
    
    
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Dummy(models.Model):
    dummy_text = models.CharField(max_length=100,default="mydummytext")
    
class Voter(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter_name = models.CharField(max_length=200, null=False)
    voter_email = models.EmailField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.voter_name