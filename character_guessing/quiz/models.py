from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    image = models.ImageField(upload_to='characters/')
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    likes = models.PositiveIntegerField(default=0)

    def is_correct(self, selected_answer):
        return selected_answer == self.correct_answer

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    liked_questions = models.ManyToManyField(Question, blank=True)