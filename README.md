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
