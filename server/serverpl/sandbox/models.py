from django.db import models

# Create your models here.

class Sandbox(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    url =  models.CharField(max_length=860, null = False)
