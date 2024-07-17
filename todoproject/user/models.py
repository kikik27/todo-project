from django.db import models

# Create your models here.

class Users(models.Model):
  id = models.BigAutoField(primary_key=True),
  name = models.CharField(max_length=225)
  email = models.CharField(max_length=225, unique=True)
  password = models.CharField(max_length=225)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
