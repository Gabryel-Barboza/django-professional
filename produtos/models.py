import uuid

from django.conf import settings
from django.db import models


class Category(models.Model):
    """
    ─── UUID como Primary Key ─────────────────────────────────────────
    Em vez do auto-increment padrão (id = Integer), usamos UUID (128 bits).

    🛡️ MITIGAÇÃO DE ATAQUES IDOR (Insecure Direct Object Reference):
    IDOR ocorre quando um atacante MANIPULA um identificador na URL para
    acessar recursos não autorizados. Exemplo clássico com IDs sequenciais:
      /usuario/3 → atacante troca para /usuario/4 e vê dados de outro usuário

    UUID resolve isso porque:
      - Impossível "adivinhar" URLs válidas (/produto/a47b... vs /produto/5)
      - Não expõe a quantidade total de registros na base
      - Geração descentralizada (não precisa de sequence, sem contenção)
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Categoria', max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name


class Product(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
    )
    image = models.ImageField(
        'Imagem do Produto', upload_to='produtos/%Y/%m/%d', blank=True, null=True
    )
    name = models.CharField('Nome do Produto', max_length=200)
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    stock = models.IntegerField('Quantidade em Estoque', default=0)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.name


# ─── Order + OrderItem ──────────────────────────────────────────────
# Modelos para o exemplo de Writable Nested Serializer.
# Order representa um PEDIDO, OrderItem os ITENS dentro do pedido.
# A relação é: Order 1 → N OrderItem (FK reversa via related_name='items')
#
# O serializer aninhado permite criar pedido + itens em UMA requisição,
# com transaction.atomic() e F() para baixa automática de estoque.

class Order(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
    )
    created_at = models.DateTimeField('Data do Pedido', auto_now_add=True)
    paid = models.BooleanField('Pago', default=False)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ('-created_at',)

    def __str__(self):
        return f'Pedido {self.uuid} — {self.user.email}'


class OrderItem(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items',
    )
    quantity = models.IntegerField('Quantidade')
    price = models.DecimalField('Preço Unitário', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    def __str__(self):
        return f'{self.quantity}x {self.product.name}'
