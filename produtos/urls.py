from django.urls import path

from .views import get_product_detail, list_products

# Roteamento para o app produtos, cria um caminho para a rota produtos/ onde a view list_products é ativada, o argumento name é usado dentro de templates para recuperar a rota automaticamente.
urlpatterns = [
    path('', list_products, name='products_list'),
    path('product/<uuid:pk>', get_product_detail, name='product_detail'),
]
