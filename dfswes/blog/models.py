from django.db import models

class Comment(models.Model):
    author = models.CharField(max_length=64)
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
