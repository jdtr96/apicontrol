from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField('Correo electronico', unique=True)
    phone_number = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username
