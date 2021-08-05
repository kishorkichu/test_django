from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=100,unique=True)
	password = models.CharField(max_length=100)
	phone = models.CharField(max_length=20)
	city = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	username = None

	USERNAME_FIELD ='email'
	REQUIRED_FIELDS =[]


