#!/usr/bin/env python
"""Django's command-line utility for administrative tasks.

┌──────────────────────────────────────────────────────────────────────┐
│ CLI — Comandos mais usados (python manage.py <comando>)              │
│                                                                      │
│   runserver         → inicia servidor de desenvolvimento             │
│   makemigrations    → cria migrations com base nas mudanças dos      │
│                       modelos (arquivos em */migrations/)            │
│   migrate           → aplica migrations pendentes ao banco real      │
│   showmigrations    → lista migrations com status (✓ aplicada)       │
│   sqlmigrate <n>    → mostra o SQL que será executado pela migration │
│   createsuperuser   → cria usuário administrador                     │
│   shell             → terminal Python com Django configurado         │
│   dbshell           → terminal SQL direto no banco configurado       │
│   collectstatic     → copia arquivos estáticos para STATIC_ROOT      │
│                                                                      │
│ 📌 SHELL_PLUS (requer django-extensions):                            │
│   python manage.py shell_plus                                        │
│   → Abre o shell com TODOS os modelos IMPORTADOS automaticamente.    │
│   → Perfeito para testar queries ORM, ver relacionamentos, debug.    │
│   → Exemplo de uso no shell_plus:                                    │
│       Product.objects.filter(price__gt=50, stock__gt=0)              │
│       Product.objects.select_related('category').all()               │
│       Category.objects.annotate(total=Count('product'))              │
└──────────────────────────────────────────────────────────────────────┘
"""

import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            'available on your PYTHONPATH environment variable? Did you '
            'forget to activate a virtual environment?'
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
