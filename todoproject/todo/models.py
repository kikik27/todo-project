from django.db import models

class Todos(models.Model):
  id = models.BigAutoField(primary_key=True)
  user_id = models.BigIntegerField()
  name = models.CharField(max_length=255)
  date = models.DateField()
  status = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
