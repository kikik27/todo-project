from django.db import models

# Create your models here.

class Users(models.Model):
  id = models.BigAutoField(primary_key=True),
  
  name = models.CharField(max_length=225)
  email = models.CharField(max_length=225, unique=True)
  password = models.CharField(max_length=225)
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  deleted_at = models.DateTimeField(auto_now=True)
  
class UserRoles(models.Model):
  id = models.BigAutoField(primary_key=True);
  user_id = models.IntegerField()
  role_id = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
class Roles(models.Model):
  id = models.BigAutoField(primary_key=True)
  name = models.CharField(max_length=255, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
