"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/

┌──────────────────────────────────────────────────────────────────────┐
│ ROTEAMENTO (URL dispatcher)                                          │
│                                                                      │
│ O Django percorre urlpatterns em ORDEM até encontrar a primeira      │
│ correspondência. A view associada é então chamada com a request.     │
│                                                                      │
│ CONCEITOS:                                                           │
│   path(route, view, name)   → rota simples (sem regex)               │
│   include()                → delega roteamento para outro arquivo    │
│   name=                    → referência reversa via {% url %}        │
│                                                                      │
│ Exemplo de adição futura:                                            │
│   path('conta/', include('users.urls')),                             │
└──────────────────────────────────────────────────────────────────────┘
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # admin.site.urls já vem com todas as views prontas (login, logout, CRUD)
    path('admin/', admin.site.urls),
    # Tudo que começa com /produtos/ é delegado ao app produtos
    path('produtos/', include('produtos.urls')),
]
