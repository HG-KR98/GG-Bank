from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    birth_date = models.DateField(null=True)
    assets = models.IntegerField(default=0)

    def __str__(self):
        return self.username
