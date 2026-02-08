from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    bio = models.TextField(blank=True)
    institution = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return self.user.username
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    points = models.IntegerField()
    due_date = models.DateField()

    def __str__(self):
        return self.title
class TaskCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'task')

class Question(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_option = models.IntegerField()

    def __str__(self):
        return self.question_text

