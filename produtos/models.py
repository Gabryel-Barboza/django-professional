import uuid

from django.db import models


# Modelos para banco de dados
class Category(models.Model):
    uuid = models.UUIDField(primary_key=True, default=True, editable=False)
    name = models.CharField('Categoria', max_length=100)
    slug = models.SlugField(unique=True)

    # Classe para personalizar as opções do modelo
    class Meta:
        # Altera o nome padrão do modelo no admin.
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name


class Product(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Relacionamento muitos para um, blank=True para formulários vazios e related_name= para nome de referência na API do Django.
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='categories',
    )
    name = models.CharField('Nome do Produto', max_length=200)
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    stock = models.IntegerField('Quantidade em Estoque', default=0)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    # O que é retornado no admin e para descrever o modelo
    def __str__(self):
        return self.name
