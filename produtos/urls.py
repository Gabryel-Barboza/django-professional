"""
URLs do App Produtos

┌──────────────────────────────────────────────────────────────────────┐
│ ROTEAMENTO POR APP                                                   │
│ Cada app tem seu próprio urls.py, incluído pelo urls.py principal    │
│ via include(). Isso organiza o projeto por domínio.                  │
│                                                                      │
│ CONVERSORES DE TIPO (path converters):                               │
│   <str:param>    →  qualquer string (default)                        │
│   <int:param>    →  apenas dígitos (converte para int)               │
│   <slug:param>   →  slug (letras, nums, hífens, underscores)         │
│   <uuid:param>   →  UUID válido (converte para uuid.UUID)            │
│   <path:param>   →  qualquer string, incluindo /                     │
│                                                                      │
│ NAME: parâmetro essencial para usar {% url 'nome' arg %} no template │
│ Se o name mudar, todos os templates que o usam precisam ser          │
│ atualizados — escolha nomes descritivos e consistentes.              │
│                                                                      │
│ ORDEM: Django testa as rotas de cima para baixo.                     │
│ Coloque rotas mais específicas ANTES das genéricas.                  │
└──────────────────────────────────────────────────────────────────────┘
"""

from django.urls import path

from .views import (
    ProductsListView,
    create_product_view,
    get_product_detail,
    list_products,
)

urlpatterns = [
    path('', list_products, name='products_list'),
    # <uuid:pk> captura um UUID da URL e converte para objeto uuid.UUID
    # Se a URL não for um UUID válido, retorna 404 automaticamente
    path('product/<uuid:pk>', get_product_detail, name='product_detail'),
    path('product/create', create_product_view, name='create_product'),
    # Usando CBVs
    path('cbv-products', ProductsListView.as_view(), name='cbv_products_list'),
]
