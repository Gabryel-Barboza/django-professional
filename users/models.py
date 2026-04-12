from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


# Criando um Custom User Class para customizar a autenticação do Django, deve ser feito antes da primeira migração do Django para não entrar em conflito com o seu próprio modelo de user.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=30, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
