"""
SINAIS (Signals) — Django

┌──────────────────────────────────────────────────────────────────────┐
│ Signals permitem executar código quando algo acontece em OUTRA       │
│ parte do sistema, sem criar acoplamento direto.                      │
│                                                                      │
│ Sinais mais comuns:                                                  │
│   pre_save     → executado ANTES de salvar o objeto no banco         │
│   post_save    → executado DEPOIS de salvar                          │
│   pre_delete   → antes de deletar                                    │
│   post_delete  → depois de deletar                                   │
│                                                                      │
│ @receiver(signal, sender=Model):                                     │
│   → Registra a função como "ouvinte" (listener) do sinal             │
│   → Quando o Model emitir o sinal, a função é chamada                │
│   → instance = objeto que está sendo salvo/deletado                  │
│                                                                      │
│ ⚠️ CUIDADO: signals são executados de forma SÍNCRONA.                │
│ Se o signal demorar, a requisição também demora.                     │
│ Para tarefas lentas (email, PDF), use Celery ou threads.             │
│                                                                      │
│ 🔁 ONDE IMPORTAR: NO ready() do AppConfig, NUNCA no topo do          │
│ models.py (evita import circular e execução prematura).              │
└──────────────────────────────────────────────────────────────────────┘
"""

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Category


@receiver(pre_save, sender=Category)
def generate_category_slug(sender, instance, **kwargs):
    """
    Gera automaticamente o slug da categoria a partir do nome,
    apenas se o slug não foi preenchido manualmente.
    Ex: "Roupas Masculinas" → "roupas-masculinas"
    """
    if not instance.slug:
        instance.slug = slugify(instance.name)
