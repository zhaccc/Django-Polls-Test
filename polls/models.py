import datetime

from django.db import models
from django.utils import timezone # ne zaboravi import za was_published_recently

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.question_text
        
    def was_published_recently(self):
        """Gleda ako je pub_date veci od timezone.now - 1 dan.
        Dakle ako je pub_date noviji od jucer vraca True."""
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1) -> old /w future bug
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    """
    Ovo ispod koristimo za admin page, da dobijemo buttons umjest
    false i promijenimo naziv rubrike u 'Published recently?'.
    """
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # sadrzi vise opcija i veze se na Question! Takodjer ovako se povezu ove dvije klase (HAS-A relationship)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text
