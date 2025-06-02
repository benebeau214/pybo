from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question') #User 모델을 FK로 글쓴이
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question') #추천인 추가

    def __str__(self):
            return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')

class Comment(models.Model):
     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_commentor')
     content = models.TextField()
     question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
     answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
     create_date = models.DateTimeField()
     modify_date = models.DateField(null=True, blank=True)



