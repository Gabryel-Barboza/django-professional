"""
DRF VIEWS — Lógica de API (REST)

┌──────────────────────────────────────────────────────────────────────┐
│ PARADIGMA STATELESS (MVT → REST API)                                │
│                                                                      │
│ No MVT tradicional (master):                                         │
│   View renderiza HTML + Template → resposta HTML                    │
│   Estado fica na sessão (cookie)                                    │
│   Servidor mantém estado do cliente                                 │
│                                                                      │
│ No REST (esta branch):                                               │
│   View retorna JSON PURO → sem sessão, sem estado                  │
│   Cada requisição contém TUDO que o servidor precisa                │
│   O cliente (React, mobile, Postman) é responsável pela UI          │
│   Autenticação via JWT (token no header Authorization)              │
│                                                                      │
│ Isso é STATELESS: o servidor não "lembra" de nada entre requests.   │
└──────────────────────────────────────────────────────────────────────┘
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Product
from .serializers import ProductSerializer


class ProductListAPIView(APIView):
    """
    ─── APIView — View baseada em classe para REST ──────────────────
    Cada método HTTP vira um método Python: get(), post(), put(), delete().
    Diferente das FBV do Django, aqui retornamos Response(JSON) em vez de render(HTML).

    ─── many=True ───────────────────────────────────────────────────
    many=True  →  o serializer espera um QuerySet/lista → JSON array [...]
    many=False →  o serializer espera UM objeto → JSON objeto {...}
    Erro comum: passar many=True para um único objeto ou vice-versa.
    """
    def get(self, request):
        products = Product.objects.select_related('category').all()
        # many=True porque products é um QuerySet (coleção de objetos)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Sem many=True porque request.data representa UM produto
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ProductViewSet(ModelViewSet):
    """
    ─── ModelViewSet — CRUD completo em poucas linhas ──────────────
    Gera automaticamente 6 ações (endpoints):
      list()           → GET    /products/
      create()         → POST   /products/
      retrieve()       → GET    /products/{pk}/
      update()         → PUT    /products/{pk}/
      partial_update() → PATCH  /products/{pk}/
      destroy()        → DELETE /products/{pk}/

    Equivalente a escrever 6 APIViews diferentes manualmente.

    ─── permission_classes ─────────────────────────────────────────
    IsAuthenticatedOrReadOnly:
      GET (leitura)   → qualquer um (autenticado ou não)
      POST/PUT/DELETE → apenas usuários autenticados (via JWT)

    ─── filter_backends ────────────────────────────────────────────
    DjangoFilterBackend → filtro exato:  ?category=<uuid>
    SearchFilter        → busca textual: ?search=termo
    OrderingFilter      → ordenação:     ?ordering=price,-created_at

    Os filtros são aplicados automaticamente pelo DRF no queryset.
    """
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'category__name']
    ordering_fields = ['price', 'created_at']
