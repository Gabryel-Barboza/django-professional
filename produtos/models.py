"""
MODELS — Camada de Dados (MVT)

┌──────────────────────────────────────────────────────────────────────┐
│ PADRÃO MVT (Model-View-Template)                                     │
│                                                                      │
│   MODEL      =  Representação dos dados (tabelas no banco)           │
│   VIEW       =  Lógica de negócio (o que fazer com os dados)         │
│   TEMPLATE   =  Apresentação (HTML que o usuário vê)                 │
│                                                                      │
│ Fluxo: URL → View busca dados no Model → renderiza Template          │
│        ↑                   ↓                                         │
│        └─────── Resposta HTTP ────────┘                              │
│                                                                      │
│ Cada classe que herda de models.Model vira uma tabela no banco.      │
│ Cada atributo da classe vira uma coluna na tabela.                   │
└──────────────────────────────────────────────────────────────────────┘
"""

import uuid

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

    Outras vantagens:
      - Escalabilidade: geração descentralizada (não precisa de sequence no banco)
      - Unicidade global: impossível colidir entre tabelas ou sistemas diferentes
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Categoria', max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        # verbose_name / verbose_name_plural: controlam a exibição NO ADMIN
        # em português, mesmo que o nome da classe/modelo esteja em inglês.
        # Útil para refatoração: podemos traduzir o código sem perder a UX.
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    # __str__: representação "amigável" do objeto.
    # Usado no admin, no shell, em logs e em foreign keys no admin.
    def __str__(self):
        return self.name


class Product(models.Model):
    """
    ─── TIPOS DE CAMPOS ──────────────────────────────────────────────
    Cada field do Django mapeia para um tipo específico no banco:
      CharField     → VARCHAR (obriga max_length)
      DecimalField  → DECIMAL (max_digits = total dígitos, decimal_places = casas decimais)
      IntegerField  → INT
      DateTimeField → DATETIME (com auto_now_add = preenche na criação)
      UUIDField     → CHAR(32) ou BINARY(16) (depende do backend)

    ─── ForeignKey (Relacionamento N:1) ───────────────────────────────
    Um Produto pertence a uma Categoria; uma Categoria tem N Produtos.
    Opções de on_delete (o que acontece se a categoria for deletada):
      CASCADE   → deleta os produtos junto com a categoria
      SET_NULL  → mantém produtos com category=NULL (precisa null=True)
      PROTECT   → impede deletar categoria se existirem produtos
      RESTRICT  → similar ao PROTECT, mas checa no final da transação
      SET_DEFAULT → atribui o valor padrão (precisa default=...)
      SET()     → executa uma função personalizada
      DO_NOTHING → integridade referencial fica a cargo do banco

    related_name: nome da "relação reversa" na API do ORM.
      Ex: categoria = Category.objects.first()
          categoria.products.all()  →  produtos daquela categoria
      Se omitido, o Django cria: categoria.product_set.all()
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
    )
    # As imagens serão salvas em: media/produtos/ANO/MES/DIA/
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
