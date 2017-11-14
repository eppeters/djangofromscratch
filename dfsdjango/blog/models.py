from django.db import models

class Comment(models.Model):
    author = models.CharField(max_length=64)
    body = models.TextField()
