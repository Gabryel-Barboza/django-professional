🚀 Django Commerce Backend - Learning Project

Este repositório foi desenvolvido com o propósito de consolidar conceitos avançados de engenharia de software e backend utilizando o ecossistema Django, integrado ao banco de dados MySQL sob infraestrutura containerizada com Docker.

O objetivo principal deste projeto não é apenas construir mais um e-commerce, mas sim dominar os padrões de mercado, boas práticas de arquitetura, otimização de consultas e segurança que diferenciam um desenvolvedor júnior de um profissional pronto para o mercado internacional.
🎯 Objetivos de Aprendizado Conquistados
1. Infraestrutura e Ambientes Isolados

    Docker & Docker Compose: Todo o ambiente (aplicação Python + banco de dados MySQL) roda de forma isolada em containers, garantindo a paridade entre os ambientes de desenvolvimento e produção.

    Segurança de Configuração: Separação estrita entre código e credenciais sensíveis através do uso de variáveis de ambiente (.env) gerenciadas pelo python-dotenv.

2. Arquitetura de Dados de Alta Performance

    Padrão Internacional: Todo o código-fonte, tabelas, campos e relacionamentos foram padronizados em inglês, mantendo a interface de gerenciamento internacionalizada em português para o usuário final através de metadados (verbose_name).

    Segurança por Design (UUIDs): Substituição de IDs sequenciais (1, 2, 3...) por identificadores únicos universais (UUIDv4) nas chaves primárias dos modelos (Product, Category, User), mitigando vulnerabilidades do tipo IDOR (Insecure Direct Object Reference).

    Custom User Model: Substituição do modelo de autenticação padrão do Django por uma classe customizada herdada de AbstractUser logo no início do projeto, preparando o ecossistema para autenticação via e-mail e extensões futuras de perfil (CPF, Foto).

3. Maestria no Django ORM & Banco de Dados (MySQL)

    Guerra ao Problema N+1: Implementação de técnicas de otimização de consultas utilizando select_related para realizar JOINs diretamente no banco, reduzindo drasticamente a carga de processamento no MySQL.

    Queries Complexas: Uso avançado de encadeamento de QuerySets, filtros textuais/numéricos e lógicas condicionais do tipo OR utilizando Q objects.

    Ciclo de Vida e Sinais (Signals): Interceptação de eventos no banco de dados através de gatilhos como pre_save para automatizar tarefas de consistência de dados (como geração de Slugs em inglês), independente de onde a requisição venha (Painel Admin ou API externa).

4. Segurança Web

    Proteção CSRF: Entendimento profundo sobre ataques de falsificação de requisições (Cross-Site Request Forgery) e como o ecossistema protege rotas de escrita através de Tokens dinâmicos (via Django Templates e Headers customizados).

🛠️ Stack Tecnológica Utilizada

    Linguagem: Python 3.11+

    Framework: Django 5+

    Banco de Dados: MySQL 8

    Ferramentas de Desenvolvimento: IPython & Django Extensions (shell_plus)

    Containerização: Docker & Docker Compose

Este projeto serve como um portfólio vivo da minha evolução técnica na stack Python/Django.

---

# Django REST Framework — Referência da API

Guia de consulta rápida para o **Django REST Framework (DRF)** — o toolkit que transforma o Django MVT em uma REST API stateless com JSON puro.

---

## Índice

- [1. REST & Paradigma Stateless](#1-rest--paradigma-stateless)
- [2. ModelSerializers (O Funil de Dados)](#2-modelserializers-o-funil-de-dados)
- [3. `many=True` — Objeto vs Coleção](#3-manytrue--objeto-vs-coleção)
- [4. Anatomia do JWT (Header, Payload, Signature)](#4-anatomia-do-jwt-header-payload-signature)
- [5. Access vs Refresh — Estratégia de Mitigação](#5-access-vs-refresh--estratégia-de-mitigação)
- [6. Simple JWT + django.contrib.auth](#6-simple-jwt--djangocontribauth)
- [7. ModelViewSet — CRUD em 3 Linhas](#7-modelviewset--crud-em-3-linhas)
- [8. DefaultRouter — Roteamento Automático](#8-defaultrouter--roteamento-automático)
- [9. Paginação Global](#9-paginação-global)
- [10. Filtros Automatizados (django-filter)](#10-filtros-automatizados-django-filter)
- [11. Writable Nested Serializers + transaction.atomic() + F()](#11-writable-nested-serializers--transactionatomic--f)

---

## 1. REST & Paradigma Stateless

### Transição Mental: MVT → REST API

| Característica | MVT (master) | REST API (esta branch) |
|---|---|---|
| **Resposta** | HTML renderizado | JSON puro |
| **Estado** | Sessão no servidor (cookie) | Stateless (token JWT no header) |
| **Cliente** | Django Templates | React, mobile, Postman |
| **Autenticação** | Sessão + CSRF | JWT (Bearer token) |
| **Rota típica** | `GET /produtos/` → HTML | `GET /products/api/products/` → JSON |

### O que muda na prática

```python
# ─── ANTES (MVT) ────────────────────────────────────────────────────
def list_products(request):
    products = Product.objects.all()
    return render(request, 'template.html', {'products': products})
# → Resposta: HTML com dados misturados à apresentação

# ─── DEPOIS (REST) ──────────────────────────────────────────────────
class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
# → Resposta: JSON puro — o cliente decide como apresentar
```

**Princípio Stateless:** cada requisição HTTP contém TODA a informação necessária para o servidor processá-la (token JWT no header `Authorization: Bearer <token>`). O servidor não armazena estado algum sobre o cliente entre requisições.

---

## 2. ModelSerializers (O Funil de Dados)

O **Serializer** é o tradutor entre objetos Python e JSON. Ele:

1. **Serializa** (Python → JSON): converte QuerySet/Model em `dict` → JSON
2. **Desserializa** (JSON → Python): valida JSON recebido → salva no banco
3. **Valida**: `validate_<campo>()` e `validate()` (análogo ao `clean_<campo>()` do Django Forms)

```python
class ProductSerializer(serializers.ModelSerializer):
    # Aninhamento (read-only): mostra dados da categoria DENTRO do JSON do produto
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('uuid', 'name', 'price', 'stock', 'created_at', 'category')

    # Validação em nível de campo (roda automaticamente no is_valid())
    def validate_price(self, value):
        if value > 50000:
            raise serializers.ValidationError('Preço excede o limite máximo')
        return value
```

### Campos mais comuns

| Campo do Serializer | Uso |
|---|---|
| `CharField()`, `IntegerField()`, `DecimalField()` | Tipos básicos |
| `SerializerMethodField()` | Campo calculado (método `get_<campo>()`) |
| `PrimaryKeyRelatedField()` | FK exibida como UUID/ID |
| `StringRelatedField()` | FK exibida como `__str__()` |
| `SlugRelatedField()` | FK exibida por um slug/campo textural |

---

## 3. `many=True` — Objeto vs Coleção

A confusão mais comum no DRF:

```python
# ❌ ERRADO: passar um QuerySet sem many=True
serializer = ProductSerializer(Product.objects.all())  # TypeError!

# ✅ CERTO: many=True para coleções
serializer = ProductSerializer(Product.objects.all(), many=True)
# → JSON: [{"uuid": "...", "name": "...", ...}, {...}]

# ✅ CERTO: many=False (padrão) para UM objeto
product = Product.objects.get(uuid='abc')
serializer = ProductSerializer(product)  # many=False implícito
# → JSON: {"uuid": "...", "name": "...", ...}
```

| `many=True` | `many=False` (padrão) |
|---|---|
| QuerySet / lista | Model / dict |
| `[]` array no JSON | `{}` objeto no JSON |
| `is_valid()` valida CADA item | `is_valid()` valida o único objeto |

---

## 4. Anatomia do JWT (Header, Payload, Signature)

Todo JWT tem 3 partes separadas por ponto (`.`):

```
┌─────────────┐   ┌──────────────────────────┐   ┌──────────────────────────────┐
│   HEADER    │   │         PAYLOAD           │   │         SIGNATURE            │
│             │   │                          │   │                              │
│ {           │   │ {                        │   │ HMAC-SHA256(                 │
│   "alg":    │   │   "token_type": "access",│   │   base64(header) + "." +     │
│    "HS256", │   │   "exp": 1717000000,     │   │   base64(payload),           │
│   "typ":    │   │   "user_id": "...",       │   │   SECRET_KEY                 │
│   "JWT"     │   │   "email": "user@..."    │   │ )                            │
│ }           │   │ }                        │   │                              │
└──────┬──────┘   └──────────┬───────────────┘   └──────────────┬───────────────┘
       │                     │                                  │
       └── Algoritmo ────────┴── Dados do token ────────────────┴── Assinatura
           HS256                                                     criptográfica
```

**Como a SECRET_KEY protege o token:**
1. O servidor gera o token: `HMAC-SHA256(header.payload, SECRET_KEY)`
2. O cliente recebe e armazena o token
3. O cliente envia o token em toda requisição: `Authorization: Bearer <token>`
4. O servidor RECALCULA a assinatura com a SECRET_KEY
5. Se o payload foi alterado → assinatura não confere → **401 Unauthorized**

> 🛡️ **IMPORTANTE**: a SECRET_KEY do Django é a MESMA usada para assinar os tokens. Se vazar, qualquer um pode forjar tokens de administrador.

---

## 5. Access vs Refresh — Estratégia de Mitigação

| Token | Duração (neste projeto) | Uso |
|---|---|---|
| **Access** | 60 minutos | Enviado no header `Authorization` para autenticar requisições |
| **Refresh** | 7 dias | Enviado para `/api/token/refresh` para obter NOVOS access tokens |

### Por que dois tokens?

```
ACCESS curto (60min)           REFRESH longo (7d)
    │                               │
    ├── Mitigação de danos:         ├── Experiência do usuário:
    │   se o token vazar,           │   não precisa logar toda hora
    │   a janela de ataque é curta  │
    │                               │
    └── Enviado em toda             └── Armazenado em secure storage
        requisição (mais exposto)       (menos exposto)
```

### Fluxo de renovação transparente (Front-end)

```javascript
// Interceptor do React/Axios:
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response.status === 401) {
      const { data } = await api.post('/api/token/refresh', { refresh });
      localStorage.setItem('access', data.access);
      error.config.headers.Authorization = `Bearer ${data.access}`;
      return api(error.config);  // re-tenta a requisição original
    }
    return Promise.reject(error);
  }
);
```

### ROTATE_REFRESH_TOKENS

```python
SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True,           # cada refresh gera UM NOVO refresh
    'BLACKLIST_AFTER_ROTATION': True,         # token anterior é invalidado
}
```

Se um refresh token for roubado e o usuário legítimo fizer refresh, o token roubado é invalidado — o atacante perde o acesso.

---

## 6. Simple JWT + django.contrib.auth

O `rest_framework_simplejwt` se acopla ao sistema de autenticação nativo do Django:

```
django.contrib.auth (User model)
        │
        ▼
Simple JWT (gera/valida tokens)
        │
        ▼
DRF (JWTAuthentication → lê o header Authorization)
        │
        ▼
ViewSets (permission_classes)
```

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# views.py
class ProductViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # GET → qualquer um
    # POST/PUT/DELETE → apenas usuários com token JWT válido
```

### permission_classes mais comuns

| Classe | Efeito |
|---|---|
| `AllowAny` | Todos acessam (público) |
| `IsAuthenticated` | Precisa de token JWT |
| `IsAuthenticatedOrReadOnly` | GET = público, POST/PUT/DELETE = autenticado |
| `IsAdminUser` | Apenas `is_staff=True` |
| `~Q()` | Custom permissions (composed via operadores lógicos) |

---

## 7. ModelViewSet — CRUD em 3 Linhas

Um `ModelViewSet` substitui **6 APIViews** separadas em uma única classe:

```python
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
```

### O que ele gera automaticamente:

| Método HTTP | Ação | Equivalente APIView manual |
|---|---|---|
| `GET /products/` | `list()` → lista paginada | `APIView.get()` + `Product.objects.all()` |
| `POST /products/` | `create()` → novo registro | `APIView.post()` + `serializer.save()` |
| `GET /products/{pk}/` | `retrieve()` → detalhe | `APIView.get(pk)` + `get_object_or_404()` |
| `PUT /products/{pk}/` | `update()` → substituição total | `APIView.put()` + `serializer.save()` |
| `PATCH /products/{pk}/` | `partial_update()` → atualização parcial | `APIView.patch()` |
| `DELETE /products/{pk}/` | `destroy()` → exclusão | `APIView.delete()` + `instance.delete()` |

### APIView vs ModelViewSet — quando usar cada um

| Cenário | Recomendado |
|---|---|
| CRUD padrão de um modelo | `ModelViewSet` + `DefaultRouter` |
| Endpoint customizado (ex: dashboard, relatório) | `APIView` |
| Operações específicas sem CRUD completo | `GenericAPIView` + mixins |

---

## 8. DefaultRouter — Roteamento Automático

O `DefaultRouter` gera automaticamente as URLs para cada ViewSet registrado:

```python
router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
urlpatterns += router.urls
```

### URLs geradas:

```
/products/api/                  →  Api root (autodescobrimento)
/products/api/products/         →  GET (list), POST (create)
/products/api/products/{pk}/    →  GET (retrieve), PUT (update), PATCH, DELETE
```

### Formato do nome das URLs (para `reverse()` ou `{% url %}`):

```
products-list       →  /products/api/products/
products-detail     →  /products/api/products/{pk}/
```

---

## 9. Paginação Global

Configuração única no `settings.py` que afeta **todos** os endpoints:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

### Formato da resposta paginada:

```json
GET /products/api/products/?page=1

{
    "count": 150,              ← total de registros
    "next": "http://...?page=3",  ← próxima página (ou null)
    "previous": "http://...?page=1", ← página anterior (ou null)
    "results": [                ← dados da página atual
        { "uuid": "...", "name": "Produto 1" },
        { "uuid": "...", "name": "Produto 2" },
        ...
    ]
}
```

### Interação com o Front-end:

```javascript
// React — rolagem infinita:
async function loadPage(page) {
    const { data } = await api.get(`/products/api/products/?page=${page}`);
    setProducts(prev => [...prev, ...data.results]);
    setHasMore(data.next !== null);
}
```

---

## 10. Filtros Automatizados (django-filter)

Três tipos de filtro configurados globalmente e customizáveis por ViewSet:

### 1. `DjangoFilterBackend` — Filtro exato

```python
# ViewSet
filterset_fields = ['category']

# Uso: GET /products/api/products/?category=<uuid>
# Retorna apenas produtos da categoria especificada
```

### 2. `SearchFilter` — Busca textual

```python
# ViewSet
search_fields = ['name', 'category__name']  # suporta lookup relacional __

# Uso: GET /products/api/products/?search=python
# Retorna produtos com "python" no nome OU no nome da categoria
# Internamente: WHERE name ILIKE '%python%' OR category__name ILIKE '%python%'
```

### 3. `OrderingFilter` — Ordenação dinâmica

```python
# ViewSet
ordering_fields = ['price', 'created_at']

# Uso: GET /products/api/products/?ordering=-price
# Retorna produtos ordenados por preço DECRESCENTE
# Múltiplos: ?ordering=-price,created_at
```

### Combinando filtros na mesma requisição:

```
GET /products/api/products/?search=python&category=<uuid>&ordering=-price
└──────────────┬────────────────┘
               └── Todos os filtros são aplicados EM CADEIA no queryset
```

---

## 11. Writable Nested Serializers + transaction.atomic() + F()

### O problema

Por padrão, serializers aninhados (ex: `items = OrderItemSerializer(many=True)`) são **read-only**. Tentar criar um pedido com itens no mesmo JSON retorna erro.

### A solução: sobrescrever `create()` com `transaction.atomic()`

```python
class OrderSerializer(serializers.ModelSerializer):
    # Aninhamento com many=True → espera um ARRAY de itens
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('uuid', 'user', 'created_at', 'paid', 'items')

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        with transaction.atomic():         # ← TUDO ou NADA
            order = Order.objects.create(**validated_data)

            for item_data in items_data:
                OrderItem.objects.create(order=order, **item_data)

                # F() expression: baixa atômica no estoque
                # O cálculo acontece no BANCO, não na RAM do Python
                Product.objects.filter(uuid=item_data['product'].uuid).update(
                    stock=F('stock') - item_data['quantity']
                )

        return order
```

### JSON esperado na criação:

```json
POST /products/api/orders/

{
    "user": "uuid-do-usuario",
    "items": [
        {"product": "uuid-produto-1", "quantity": 2, "price": 59.90},
        {"product": "uuid-produto-2", "quantity": 1, "price": 29.90}
    ]
}
```

### transaction.atomic() — O que garante:

```
┌─────────────────────────────────────────────────────────────────┐
│  INÍCIO DA TRANSAÇÃO                                            │
│                                                                 │
│  1. Order.objects.create(...)                                   │
│       ↓                                                         │
│  2. OrderItem.objects.create(order, ...)  ← item 1            │
│       ↓                                                         │
│  3. Product.stock = F('stock') - qtd      ← baixa estoque     │
│       ↓                                                         │
│  4. OrderItem.objects.create(order, ...)  ← item 2            │
│       ↓                                                         │
│  ✓ SE TUDO OK → COMMIT (dados persistidos)                    │
│  ✗ SE ALGO FALHAR → ROLLBACK (nada é salvo)                   │
└─────────────────────────────────────────────────────────────────┘
```

### F() + transaction.atomic() — Prevenção de Race Condition

```python
# ❌ PERIGOSO (race condition):
produto = Product.objects.get(uuid=...)       # 1. Lê stock=10
produto.stock -= quantidade                     # 2. Calcula 10-3=7 (em Python)
produto.save()                                  # 3. Salva stock=7
# Se 2 usuários compram ao mesmo tempo:
#   Usuário A: lê stock=10
#   Usuário B: lê stock=10 (ainda não foi salvo!)
#   A salva stock=7
#   B salva stock=7 (PERDEU UMA VENDA — deveria ser 4!)

# ✅ SEGURO (F() + atomic):
with transaction.atomic():
    Product.objects.filter(uuid=...).update(stock=F('stock') - quantidade)
    # O MySQL executa: UPDATE ... SET stock = stock - 3
    # O banco TRAVA a linha durante a operação → sem race condition
```

---

# Referência ORM Django

Guia de consulta rápida para o **Object-Relational Mapping (ORM)** do Django — a camada que traduz classes Python em tabelas SQL e vice-versa.

---

## Índice

- [1. Operações Básicas](#1-operações-básicas)
- [2. `.get()` vs `.filter()`](#2-get-vs-filter)
- [3. Lookups (Operadores de Busca)](#3-lookups-operadores-de-busca)
- [4. Solução N+1 com `select_related()`](#4-solução-n1-com-select_related)
- [5. Q Objects (Lógica OR, AND, NOT)](#5-q-objects-lógica-or-and-not)
- [6. Atualização em Lote com `.update()`](#6-atualização-em-lote-com-update)
- [7. Agregações: `aggregate()` e `annotate()`](#7-agregações-aggregate-e-annotate)
- [8. Exemplos Práticos Completos](#8-exemplos-práticos-completos)

---

## 1. Operações Básicas

> **Manager:** `objects` é o `Manager` padrão de todo modelo. É a porta de entrada para consultas.

```python
from produtos.models import Product, Category

# ─── CRUD ─────────────────────────────────────────────────────────────

# CREATE
produto = Product.objects.create(
    name='Camiseta Python',
    price=59.90,
    stock=10,
)

# READ (todos)
todos = Product.objects.all()          # SELECT * FROM produtos_product

# READ (filtrado)
disponiveis = Product.objects.filter(stock__gt=0)

# READ (um objeto)
produto = Product.objects.get(uuid='abc-123')

# UPDATE
produto.price = 69.90
produto.save()

# DELETE
produto.delete()

# ─── CONTAGEM ─────────────────────────────────────────────────────────
total = Product.objects.count()        # SELECT COUNT(*) FROM produtos_product

# ─── ORDENAÇÃO ────────────────────────────────────────────────────────
Product.objects.order_by('price')       # ASC
Product.objects.order_by('-price')      # DESC
Product.objects.order_by('category', 'price')  # composta

# ─── LIMIT / OFFSET ───────────────────────────────────────────────────
Product.objects.all()[0:5]              # LIMIT 5 (slicing do QuerySet)
Product.objects.all()[5:10]             # LIMIT 5 OFFSET 5
```

---

## 2. `.get()` vs `.filter()`

A principal fonte de bugs para iniciantes. Entenda a diferença:

| Característica | `.get(**kwargs)` | `.filter(**kwargs)` |
|---|---|---|
| **Retorno** | Um objeto | `QuerySet` (sempre) |
| **0 resultados** | Lança `Model.DoesNotExist` | `QuerySet` vazio (`[]`) |
| **2+ resultados** | Lança `Model.MultipleObjectsReturned` | `QuerySet` com N itens |
| **Uso típico** | Detalhe de um registro | Listas e buscas abertas |

```python
# .get() — use quando DEVE existir exatamente 1 registro
try:
    produto = Product.objects.get(uuid='abc-123')
except Product.DoesNotExist:
    # tratar erro
    pass

# 📌 Em views: sempre prefira get_object_or_404()
from django.shortcuts import get_object_or_404
produto = get_object_or_404(Product, pk='abc-123')
# → já retorna HTTP 404 automaticamente

# .filter() — use para listas (0, 1 ou N resultados)
produtos = Product.objects.filter(stock__gt=0)
for p in produtos:          # seguro mesmo se vazio
    print(p.name)
```

---

## 3. Lookups (Operadores de Busca)

Sufixos com `__` (duplo underscore) que refinam a consulta no banco:

### 3.1. Texto

| Lookup | SQL gerado | Uso |
|---|---|---|
| `exact` | `= 'valor'` | `name__exact='Camiseta'` (padrão, pode omitir) |
| `iexact` | `LIKE 'valor'` | `name__iexact='camiseta'` (case-insensitive) |
| `contains` | `LIKE '%valor%'` | `name__contains='Camis'` |
| `icontains` | `LIKE '%valor%'` | `name__icontains='camis'` ← mais usado |
| `startswith` | `LIKE 'valor%'` | `name__startswith='Cam'` |
| `istartswith` | `LIKE 'valor%'` | `name__istartswith='cam'` |

### 3.2. Números e Datas

| Lookup | Significado | Exemplo |
|---|---|---|
| `gt` | maior que (`>`) | `price__gt=50` |
| `gte` | maior ou igual (`>=`) | `stock__gte=10` |
| `lt` | menor que (`<`) | `price__lt=100` |
| `lte` | menor ou igual (`<=`) | `stock__lte=5` |
| `in` | está em uma lista | `price__in=[10, 20, 30]` |
| `range` | entre dois valores | `price__range=(10, 100)` |

### 3.3. Nulos e Negação

| Lookup | Exemplo | Efeito |
|---|---|---|
| `isnull` | `category__isnull=True` | É nulo |
| `exclude()` | `Product.objects.exclude(stock=0)` | Negação (`NOT`) |

### 3.4. Data (partes)

```python
Product.objects.filter(created_at__year=2026)
Product.objects.filter(created_at__month=5)
Product.objects.filter(created_at__day=31)
Product.objects.filter(created_at__week_day=1)  # 1 = domingo
```

### 3.5. Exemplos combinados

```python
# Preço maior que 50 E menor que 200
Product.objects.filter(price__gt=50, price__lt=200)

# Nome contém "python" (case-insensitive) E estoque > 0
Product.objects.filter(name__icontains='python', stock__gt=0)

# Criados em 2026 OU preço menor que 10 (precisa de Q — veja seção 5)
Product.objects.filter(Q(created_at__year=2026) | Q(price__lt=10))
```

---

## 4. Solução N+1 com `select_related()`

### O Problema N+1

```python
# ISSO é N+1 — NUNCA faça em listas com ForeignKey:
produtos = Product.objects.all()          # 1 query
for p in produtos:
    print(p.category.name)                # +N queries (uma para cada produto)
# Total: 1 + N queries = devastador para performance
```

### A Solução

```python
# ISSO resolve — select_related faz JOIN em UMA query:
produtos = Product.objects.select_related('category').all()
for p in produtos:
    print(p.category.name)  # 0 queries extras (já veio no JOIN)
# Total: 1 query
```

### Quando usar

| Quando | Usar | Motivo |
|---|---|---|
| FK p/ um único objeto | `select_related()` | Faz JOIN (uma query) |
| M2M ou relação reversa | `prefetch_related()` | 2 queries otimizadas |

> **Regra prática:** toda vez que você acessa `objeto.relacionamento` dentro de um loop, você precisa de `select_related()` ou `prefetch_related()`.

---

## 5. Q Objects (Lógica OR, AND, NOT)

Por padrão, `filter()` com múltiplos argumentos usa **AND**. Para **OR** (ou combinações complexas), use `Q` objects.

```python
from django.db.models import Q

# ─── OR (|) ───────────────────────────────────────────────────────────
# Preço > 100 OU estoque = 0
Product.objects.filter(Q(price__gt=100) | Q(stock=0))

# ─── AND (&) ──────────────────────────────────────────────────────────
# Equivalente ao filter padrão (explícito)
Product.objects.filter(Q(price__gt=50) & Q(stock__gt=0))
# Mesmo que: Product.objects.filter(price__gt=50, stock__gt=0)

# ─── NOT (~) ──────────────────────────────────────────────────────────
# Produtos que NÃO são de uma categoria específica
Product.objects.filter(~Q(category=categoria))

# ─── COMBINAÇÃO COMPLEXA ──────────────────────────────────────────────
# (nome contém "promo" OU preço < 20) E estoque > 0
Product.objects.filter(
    Q(name__icontains='promo') | Q(price__lt=20),
    stock__gt=0
)
```

---

## 6. Atualização em Lote com `.update()`

Atualiza diretamente no banco **sem carregar objetos na memória**:

```python
# ✅ Rápido (1 query, não carrega objetos)
Product.objects.filter(category=categoria).update(stock=0)

# ❌ Lento (N queries + carrega N objetos na memória)
for p in Product.objects.filter(category=categoria):
    p.stock = 0
    p.save()
```

### ⚠️ Atenção

`.update()` **não emite** os sinais `pre_save` / `post_save`. Se sua aplicação depende de signals (ex: gerar log, invalidar cache), use iteração com `.save()`.

```python
# Alternativa que EMITE signals (mas é mais lenta):
for p in Product.objects.filter(category=categoria):
    p.stock = 0
    p.save()  # → dispara pre_save e post_save
```

---

## 7. Agregações: `aggregate()` e `annotate()`

```python
from django.db.models import Count, Sum, Avg, Max, Min
```

### `aggregate()` — Totais Globais

Retorna um **dicionário** com valores calculados sobre TODOS os registros:

```python
# Única agregação
resultado = Product.objects.aggregate(total=Sum('stock'))
# → {'total': 1547}

# Múltiplas agregações de uma vez
estatisticas = Product.objects.aggregate(
    total_estoque=Sum('stock'),
    media_preco=Avg('price'),
    mais_caro=Max('price'),
    mais_barato=Min('price'),
    quantidade=Count('id'),
)
# → {'total_estoque': 1547, 'media_preco': 89.5, 'mais_caro': 299.90, ...}
```

### `annotate()` — Colunas Calculadas por Grupo

Adiciona uma coluna **virtual** a CADA objeto do `QuerySet`:

```python
# Quantos produtos cada categoria tem?
from django.db.models import Count

categorias = Category.objects.annotate(
    total_produtos=Count('products')  # 'products' = related_name de Product
)

for cat in categorias:
    print(f'{cat.name}: {cat.total_produtos} produtos')

# Preço médio por categoria
categorias = Category.objects.annotate(
    preco_medio=Avg('products__price')
)
```

### `aggregate()` vs `annotate()` — Resumo

| | `aggregate()` | `annotate()` |
|---|---|---|
| **Retorno** | `dict` | `QuerySet` (cada objeto ganha um atributo novo) |
| **Escopo** | Global (todos os registros) | Por grupo/objeto |
| **SQL** | `SELECT AVG(...) FROM ...` | `SELECT ..., AVG(...) FROM ... GROUP BY ...` |
| **Exemplo** | Preço médio TOTAL | Preço médio POR CATEGORIA |

---

## 8. Exemplos Práticos Completos

```python
# ─── CENÁRIO 1: Vitrine de produtos disponíveis ──────────────────────
def vitrine(request):
    produtos = Product.objects \
        .select_related('category') \
        .filter(stock__gt=0) \
        .order_by('-created_at')
    return render(request, 'vitrine.html', {'produtos': produtos})

# ─── CENÁRIO 2: Busca com múltiplos filtros ──────────────────────────
def buscar(request):
    query = request.GET.get('q', '')
    preco_max = request.GET.get('preco_max')

    produtos = Product.objects.select_related('category')

    if query:
        produtos = produtos.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query)
        )
    if preco_max:
        produtos = produtos.filter(price__lte=preco_max)

    return render(request, 'busca.html', {'produtos': produtos})

# ─── CENÁRIO 3: Relatório de estoque ─────────────────────────────────
def relatorio(request):
    categorias = Category.objects.annotate(
        total_produtos=Count('products'),
        valor_total=Sum('products__price'),
        estoque_total=Sum('products__stock'),
    ).order_by('-total_produtos')

    return render(request, 'relatorio.html', {'categorias': categorias})

# ─── CENÁRIO 4: Zerar estoque de uma categoria ───────────────────────
def zerar_estoque(request, categoria_uuid):
    categoria = get_object_or_404(Category, pk=categoria_uuid)
    Product.objects.filter(category=categoria).update(stock=0)
    return redirect('relatorio')
```

---

## 9. `prefetch_related()` — O irmão do `select_related()` para M2M e Relações Reversas

```python
from django.db.models import Prefetch
```

### select_related vs prefetch_related

| Característica | `select_related()` | `prefetch_related()` |
|---|---|---|
| **Tipo de relação** | FK direta (1:1, N:1) | M2M, FK reversa (1:N) |
| **Estratégia** | `JOIN` SQL (uma query) | Query separada + combinação em Python |
| **Performance** | Excelente para FKs diretas | Excelente para coleções reversas |
| **Exemplo** | `product.category` | `category.products.all` |

### O problema N+1 reverso

```python
# ISSO é N+1 — cada categoria faz uma query extra pelos produtos:
categorias = Category.objects.all()                # 1 query
for cat in categorias:
    print(cat.products.all())                      # +N queries (uma por categoria)
# Total: 1 + N queries
```

### A solução

```python
# prefetch_related carrega TUDO em 2 queries no total:
categorias = Category.objects.prefetch_related('products').all()  # 2 queries
for cat in categorias:
    print(cat.products.all())  # 0 queries extras (já está na memória)
# Total: 2 queries (1 p/ categorias + 1 p/ todos os produtos)
```

### Combinando `select_related()` + `prefetch_related()`

```python
# Cenário real: categorias com produtos, cada produto com sua categoria
categorias = Category.objects.prefetch_related(
    Prefetch(
        'products',
        queryset=Product.objects.select_related('category')
    )
).all()
```

### prefetch_related com filtros (usando `Prefetch`)

```python
from django.db.models import Prefetch

# Carrega apenas produtos com estoque > 0
categorias = Category.objects.prefetch_related(
    Prefetch(
        'products',
        queryset=Product.objects.filter(stock__gt=0),
        to_attr='produtos_disponiveis'  # nome do atributo no objeto
    )
).all()

for cat in categorias:
    # cat.produtos_disponiveis → lista filtrada (não é QuerySet!)
    for p in cat.produtos_disponiveis:
        print(p.name)
```

---

## 10. `F()` Expressions — Operações no Banco (Atomicidade)

```python
from django.db.models import F
```

### O problema: Race Condition

```python
# ISSO NÃO É SEGURO em sistemas concorrentes:
for p in produtos:
    p.stock = p.stock - quantidade_comprada
    p.save()

# Problema: se 2 usuários compram ao mesmo tempo:
# Usuário A lê stock=10, Usuário B lê stock=10
# A salva stock=5, B salva stock=5 (perdeu uma venda!)
```

### A solução: `F()` delega o cálculo para o MySQL

```python
# F() expression: o cálculo acontece NO BANCO, não na memória do Python
from django.db.models import F

# UPDATE produtos_product SET stock = stock - 2
Product.objects.filter(uuid=produto.uuid).update(stock=F('stock') - 2)

# Vantagens:
#   1. Atômico: o banco trava a linha durante a operação
#   2. Rápido: não carrega objeto na memória (1 query apenas)
#   3. Sem race condition: o MySQL processa sequencialmente
```

### Outros usos de `F()`

```python
# Aumentar preço em 10% para todos os produtos
Product.objects.update(price=F('price') * 1.10)

# Comparar campos entre si
Product.objects.filter(stock=F('stock_anterior'))  # stock = stock_anterior

# Em filter também funciona
Product.objects.filter(stock__lt=F('stock_maximo'))

# Com anotações
from django.db.models import F, Value
from django.db.models.functions import Concat

Product.objects.annotate(
    nome_e_categoria=Concat(F('name'), Value(' - '), F('category__name'))
)
```

---

## 11. `Case/When` — Lógica Condicional Direto no SQL

```python
from django.db.models import Case, When, Value, IntegerField, CharField
```

### Classificação condicional (IF/ELSE no banco)

```python
from django.db.models import Case, When, Value, CharField

# Cria coluna 'status_estoque' com texto classificado
produtos = Product.objects.annotate(
    status_estoque=Case(
        When(stock=0, then=Value('Esgotado')),
        When(stock__lt=5, then=Value('Estoque Crítico')),
        When(stock__lt=20, then=Value('Estoque Baixo')),
        default=Value('Estoque OK'),
        output_field=CharField(),
    )
)

for p in produtos:
    print(f'{p.name}: {p.status_estoque}')
    # → "Camiseta Python: Estoque OK"
    # → "Teclado Mecânico: Estoque Crítico"
```

### Case/When com números (cálculo de faixas)

```python
from django.db.models import Case, When, Value, IntegerField

# Faixa de preço (categorização)
produtos = Product.objects.annotate(
    faixa_preco=Case(
        When(price__lt=50, then=Value(1)),    # Barato
        When(price__lt=150, then=Value(2)),   # Médio
        When(price__lt=500, then=Value(3)),   # Caro
        default=Value(4),                      # Premium
        output_field=IntegerField(),
    )
)

# Ordenar por faixa de preço (do mais barato ao mais caro)
produtos = produtos.order_by('faixa_preco', 'price')

# Agrupar por faixa
from django.db.models import Count
faixas = produtos.values('faixa_preco').annotate(total=Count('id'))
```

### Por que fazer no banco vs no Python?

| No Python | No SQL (Case/When) |
|---|---|
| Carrega todos os objetos na memória | Só o resultado |
| Processamento serial (1 core) | Paralelo no banco |
| O(N) operações em RAM | O(N) no banco (mais eficiente) |
| Ideal para poucos registros | Ideal para MUITOS registros |

---

## 12. Renderizando Relações no Template (Loops Aninhados)

Quando você tem uma relação N:1 e precisa exibir dados relacionados no template, existem duas abordagens:

### Abordagem 1: Uma FK com `select_related` (mais comum)

```python
# view
produtos = Product.objects.select_related('category').all()
```

```html
{# template #}
<ul>
  {% for product in products %}
    <li>
      {{ product.name }}
      {# 🔁 product.category JÁ está carregado (select_related) #}
      <small>Categoria: {{ product.category.name }}</small>
    </li>
  {% endfor %}
</ul>
```

### Abordagem 2: Lista de categorias com produtos dentro (relação reversa)

```python
# view
categorias = Category.objects.prefetch_related('products').all()
```

```html
{# template — loop aninhado #}
{% for category in categorias %}
  <h2>{{ category.name }}</h2>
  <ul>
    {# category.products.all → já está em memória (prefetch_related) #}
    {# Sem prefetch_related, cada iteração faria 1 query extra!     #}
    {% for product in category.products.all %}
      <li>{{ product.name }} — R$ {{ product.price|floatformat:2 }}</li>
    {% empty %}
      <li>Nenhum produto nesta categoria</li>
    {% endfor %}
  </ul>
{% endfor %}
```

### Regra de Ouro para Templates com Relacionamentos

> **Se você acessa `objeto.relacionamento` dentro de um `{% for %}` no template,
> você PRECISA de `select_related()` (FK direta) ou `prefetch_related()` (FK reversa/M2M)
> na view. Caso contrário, cada iteração gera uma query = N+1.**

### Consulta de performance no Django Debug Toolbar

```python
# Adicione ao INSTALLED_APPS (apenas em dev):
INSTALLED_APPS += ['debug_toolbar']

# Ele mostra:
# ✔ Quantas queries foram executadas
# ✔ Quanto tempo cada query levou
# ✔ Se há queries duplicadas (N+1)
# ✔ O SQL de cada query
```

---

## 13. Índice de Referência Rápida

| Operação | Método | SQL gerado |
|---|---|---|
| Buscar todos | `.all()` | `SELECT * FROM ...` |
| Filtrar | `.filter(campo=valor)` | `WHERE campo = valor` |
| Um objeto | `.get(pk=1)` | `WHERE id = 1 LIMIT 1` |
| OR lógico | `Q(a=1) \| Q(b=2)` | `WHERE a = 1 OR b = 2` |
| NOT | `~Q(campo=valor)` | `WHERE NOT campo = valor` |
| JOIN FK | `.select_related('fk')` | `LEFT JOIN ... ON ...` |
| Pré-carregar reverso | `.prefetch_related('nome_set')` | 2 queries |
| Atualizar lote | `.update(campo=valor)` | `UPDATE ... SET ...` |
| Agregar | `.aggregate(Sum('campo'))` | `SELECT SUM(...)` |
| Anotar | `.annotate(Count('rel'))` | `GROUP BY ...` |
| Operação atômica | `F('campo') + 1` | `campo = campo + 1` |
| Condicional SQL | `Case/When` | `CASE WHEN ... END` |

