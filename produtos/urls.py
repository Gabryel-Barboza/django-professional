"""
URLs do App Produtos (REST API)

┌──────────────────────────────────────────────────────────────────────┐
│ DefaultRouter — ROTEAMENTO AUTOMÁTICO para ViewSets                 │
│                                                                      │
│ Diferente de path() manual, o router.register() gera 6 URLs:        │
│                                                                      │
│ Método  | Rota                              | Ação (ViewSet)        │
│─────────|───────────────────────────────────|───────────────────────│
│ GET     | /products/api/products/           | list()                │
│ POST    | /products/api/products/           | create()              │
│ GET     | /products/api/products/{uuid}/    | retrieve()            │
│ PUT     | /products/api/products/{uuid}/    | update()              │
│ PATCH   | /products/api/products/{uuid}/    | partial_update()      │
│ DELETE  | /products/api/products/{uuid}/    | destroy()             │
│                                                                      │
│ basename='products' → as URLs são nomeadas como:                    │
│   products-list, products-detail (para usar em reverse())           │
│                                                                      │
│ O router também gera um root view em /products/api/ listando        │
│ todos os endpoints registrados (autodescobrimento da API).          │
└──────────────────────────────────────────────────────────────────────┘
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductListAPIView, ProductViewSet

# ─── Registra o ViewSet no router ──────────────────────────────────
# O router "observa" o ViewSet e cria automaticamente as 6 URLs acima.
# Se adicionar novos ViewSets, basta registrar aqui.
router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')

urlpatterns = [
    # APIView manual (GET + POST)
    path('', ProductListAPIView.as_view(), name='products_list'),
    # URLs automáticas do ViewSet (list, create, retrieve, update, partial_update, destroy)
    path('api/', include(router.urls)),
]
