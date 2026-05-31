"""
VIEWS — Lógica de Negócio (MVT)

┌──────────────────────────────────────────────────────────────────────┐
│ Funções abaixo recebem um HttpRequest e retornam um HttpResponse.    │
│ O Django injeta automaticamente a request vinda do roteamento (URL). │
│                                                                      │
│ render() = shortcut que:                                             │
│   1. Carrega o template                                              │
│   2. Preenche com o context dict                                     │
│   3. Retorna um HttpResponse pronto                                  │
└──────────────────────────────────────────────────────────────────────┘
"""

from django.shortcuts import get_object_or_404, render

from .models import Product


def list_products(request):
    # ─── ORM: .all() ────────────────────────────────────────
    # SELECT * FROM produtos_product;
    # Retorna um QuerySet com TODOS os objetos da tabela.
    products = Product.objects.all()

    # ─── ORM: .filter() vs .get() ───────────────────────────
    # .filter(**kwargs)  →  SEMPRE retorna QuerySet (0, 1, ou N itens)
    #                        NUNCA lança exceção. Usar para listas.
    #   Ex: Product.objects.filter(stock__gt=0)
    #
    # .get(**kwargs)     →  retorna UM objeto OU lança exceção:
    #                        - Model.DoesNotExist (se não achar)
    #                        - Model.MultipleObjectsReturned (se >1)
    #   Ex: Product.objects.get(uuid='abc-123')
    #
    # 📌 Em views, prefira get_object_or_404() → já retorna HTTP 404

    # ─── ORM: select_related() → Combate N+1 ────────────────
    # Problema N+1: ao iterar products e acessar product.category
    # para CADA item, o Django faz 1 query + N queries (uma por FK).
    #
    # select_related('category') faz um JOIN SQL e carrega TUDO
    # em UMA ÚNICA consulta → performance muito superior.
    #
    # 🔁 Uso: Product.objects.select_related('category').all()
    #
    # (Não aplicado abaixo porque é um exemplo simples, mas essencial
    #  saber quando a lista crescer)

    context = {'products_list': products, 'title': 'Nossa Vitrine'}
    return render(request, 'produtos/productsList.html', context)


def get_product_detail(request, pk):
    # get_object_or_404 = .get() + Http404 se não existir
    # pk = primary key (pode ser int, UUID, etc — depende do modelo)
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'produtos/productDetail.html', context)
