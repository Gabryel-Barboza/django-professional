"""
SINAIS (Signals) — Django

┌──────────────────────────────────────────────────────────────────────┐
│ Signals permitem executar código quando algo acontece em OUTRA      │
│ parte do sistema, sem criar acoplamento direto.                     │
│                                                                      │
│ Sinais mais comuns:                                                  │
│   pre_save     → executado ANTES de salvar o objeto no banco        │
│   post_save    → executado DEPOIS de salvar                         │
│   pre_delete   → antes de deletar                                   │
│   post_delete  → depois de deletar                                  │
│                                                                      │
│ @receiver(signal, sender=Model):                                     │
│   → Registra a função como "ouvinte" (listener) do sinal            │
│   → Quando o Model emitir o sinal, a função é chamada              │
│   → instance = objeto que está sendo salvo/deletado                │
│                                                                      │
│ ⚠️ CUIDADO: signals são executados de forma SÍNCRONA.              │
│ Se o signal demorar, a requisição também demora.                   │
│ Para tarefas lentas (email, PDF), use Celery ou threads.           │
│                                                                      │
│ 🔁 ONDE IMPORTAR: NO ready() do AppConfig, NUNCA no topo do        │
│ models.py (evita import circular e execução prematura).            │
│                                                                      │
│ post_delete + arquivos:                                             │
│   Quando um objeto com FileField/ImageField é deletado, o arquivo   │
│   no disco NÃO é removido automaticamente. O signal post_delete    │
│   permite limpar o arquivo manualmente após a exclusão do registro. │
└──────────────────────────────────────────────────────────────────────┘
"""

import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Category, Product


@receiver(pre_save, sender=Category)
def generate_category_slug(sender, instance, **kwargs):
    """
    Gera automaticamente o slug da categoria a partir do nome,
    apenas se o slug não foi preenchido manualmente.
    Ex: "Roupas Masculinas" → "roupas-masculinas"
    """
    if not instance.slug:
        instance.slug = slugify(instance.name)


@receiver(pre_save, sender=Product)
def capitalize_product_name(sender, instance, **kwargs):
    """
    Capitaliza as iniciais do nome do produto antes de salvar.
    Ex: "camiseta pyThon" → "Camiseta Python"

    Executado em CADA save() (criação e alteração),
    independentemente se o formulário validou ou não.
    """
    if instance.name:
        instance.name = instance.name.title()


@receiver(post_delete, sender=Product)
def remove_product_image(sender, instance, **kwargs):
    """
    Remove o arquivo de imagem do disco quando o produto é deletado.

    ⚠️ instance já foi deletada do BANCO, mas o objeto ainda está
    na memória com os atributos (instance.image.path) disponíveis.

    Por que isso não é automático?
    - Performance: deletar arquivos é I/O caro
    - Segurança: pode haver links simbólicos ou referências externas
    - Decisão de design: o Django prefere não assumir que você quer
      deletar arquivos que podem ser usados em outros lugares
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
