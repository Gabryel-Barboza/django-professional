"""
CUSTOM USER MODEL — Modelo de Usuário Personalizado

┌──────────────────────────────────────────────────────────────────────┐
│ Por que criar um Custom User Model?                                  │
│   1. Adicionar campos extras (cpf, data de nascimento, etc.)         │
│   2. Trocar o campo de login (email em vez de username)              │
│   3. Usar UUID como primary key (mais seguro que ID sequencial)      │
│                                                                      │
│ ⚠️ REGRA DE OURO: deve ser definido ANTES da primeira migração.      │
│ Depois que o banco já foi criado, migrar o modelo de usuário é       │
│ extremamente complexo (envolve migration de dados e riscos).         │
│                                                                      │
│ AbstractUser vs AbstractBaseUser:                                    │
│   AbstractUser                                                       │
│     → Já inclui: username, email, first_name, last_name, password,   │
│       is_staff, is_superuser, is_active, date_joined, groups,        │
│       user_permissions                                               │
│     → Bom para 95% dos casos (inclusive este)                        │
│                                                                      │
│   AbstractBaseUser                                                   │
│     → Só inclui: password, last_login                                │
│     → Para quando você quer um modelo de usuário COMPLETAMENTE       │
│       diferente (ex: login por CPF + senha, sem username)            │
│     → Exige implementar: BaseUserManager customizado                 │
└──────────────────────────────────────────────────────────────────────┘
"""

from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    ─── USERNAME_FIELD ────────────────────────────────────────────────
    Define qual campo é usado para autenticação (login).
    Padrão do Django: 'username'
    Nosso projeto: 'email' → login com email e senha.

    ─── REQUIRED_FIELDS ───────────────────────────────────────────────
    Campos solicitados ao criar superuser (além do USERNAME_FIELD e password).
    Aqui: ['username'] (username ainda é obrigatório, mas não é o login).

    ─── UUID como PK ──────────────────────────────────────────────────
    Em vez de id auto-increment (1, 2, 3...), usamos UUID (128 bits).
    Vantagens:
      - Ofuscação: atacante não consegue "adivinhar" IDs de usuários
      - Escalabilidade: geração única sem consulta ao banco
      - Unificação: mesmo padrão dos outros models do projeto

    ─── unique=True ───────────────────────────────────────────────────
    Garante unicidade no banco (cria índice único).
    Impede duplicatas de email e CPF em nível de banco de dados.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=30, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
