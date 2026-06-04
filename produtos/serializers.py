"""
SERIALIZERS — O "Funil" entre ORM e JSON

┌──────────────────────────────────────────────────────────────────────┐
│ ModelSerializer: traduz objetos Python complexos (QuerySet,          │
│ datetime, Decimal, UUID) em JSON puro para trafegar na rede,       │
│ e reconstrói objetos Python a partir de JSON recebido.              │
│                                                                      │
│ many=True  →  espera LISTA/QuerySet → JSON array [...]              │
│ many=False →  espera UM objeto      → JSON objeto {...}             │
│                                                                      │
│ Serializers aninhados (read-only):                                   │
│   Um campo pode ser OUTRO serializer, exibindo dados relacionados   │
│   dentro do JSON. Por padrão, são READ-ONLY — não aceitam escrita.  │
│                                                                      │
│ Writable Nested Serializers:                                         │
│   Para permitir ESCRITA aninhada, é necessário SOBRESCREVER         │
│   o método create() e/ou update() do serializer pai, combinado      │
│   com transaction.atomic() para garantir atomicidade.               │
│   O padrão é: criar o pai → criar os filhos → atualizar estoque.   │
└──────────────────────────────────────────────────────────────────────┘
"""

from django.db import transaction
from django.db.models import F

from rest_framework import serializers

from .models import Category, Order, OrderItem, Product


# ─── CategorySerializer ─────────────────────────────────────────────
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('uuid', 'name', 'slug')


# ─── ProductSerializer ──────────────────────────────────────────────
class ProductSerializer(serializers.ModelSerializer):
    # Aninhamento read-only: ao serializar, mostra os dados completos
    # da categoria DENTRO do JSON do produto, em vez de só o UUID.
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('uuid', 'name', 'price', 'stock', 'created_at', 'category')

    # ─── Validação em nível de campo ────────────────────────────────
    # O DRF chama automaticamente validate_<campo>() durante is_valid().
    # Funciona como o clean_<campo>() dos ModelForms do Django.
    def validate_price(self, value):
        if value > 50000:
            raise serializers.ValidationError(
                'O preço inserido ultrapassa o limite máximo de R$50.000,00'
            )
        return value


# ─── OrderItemSerializer ────────────────────────────────────────────
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('uuid', 'product', 'quantity', 'price')


# ─── OrderSerializer (Writable Nested) ──────────────────────────────
class OrderSerializer(serializers.ModelSerializer):
    # Aninhamento WRITABLE: items é uma lista de objetos JSON.
    # Para isso funcionar, precisamos sobrescrever create().
    #
    # many=True significa que items espera um ARRAY no JSON:
    #   "items": [{"product": "...", "quantity": 2, "price": 59.90}, ...]
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('uuid', 'user', 'created_at', 'paid', 'items')
        read_only_fields = ('uuid', 'created_at')

    def create(self, validated_data):
        """
        ─── Writable Nested Create com transaction.atomic() ──────────

        O formato esperado do JSON:
        {
            "user": "uuid-do-usuario",
            "items": [
                {"product": "uuid-produto-1", "quantity": 2, "price": 59.90},
                {"product": "uuid-produto-2", "quantity": 1, "price": 29.90}
            ]
        }

        transaction.atomic():
          - Se QUALQUER operação falhar (ex: produto não encontrado),
            TUDO é desfeito (rollback) — o pedido não é criado parcialmente.
          - Garante integridade: ou o pedido completo é salvo, ou nada é salvo.

        F() expression (baixa de estoque):
          - Product.objects.filter(...).update(stock=F('stock') - quantity)
          - O cálculo acontece no BANCO, não na memória do Python
          - Atômico: sem race condition se 2 pedidos acontecerem ao mesmo tempo

        🛡️ Fluxo completo:
          1. Cria o Order
          2. Para cada item, cria OrderItem
          3. Dá baixa no estoque usando F()
          4. Se algo falhar → transaction.atomic() faz rollback total
        """
        items_data = validated_data.pop('items')

        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item_data in items_data:
                OrderItem.objects.create(order=order, **item_data)

                # F() expression: baixa atômica no estoque
                # UPDATE produtos_product SET stock = stock - quantity WHERE uuid = ...
                Product.objects.filter(uuid=item_data['product'].uuid).update(
                    stock=F('stock') - item_data['quantity']
                )

        return order
