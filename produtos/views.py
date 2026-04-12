from django.shortcuts import get_object_or_404, render

from .models import Product


# Create your views here.
def list_products(request):
    products = Product.objects.all()

    # Context é o dicionário passado para render substituir no template cada variável.
    context = {'products_list': products, 'title': 'Nossa Vítrine'}

    return render(request, 'produtos/productsList.html', context)


def get_product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}

    return render(request, 'produtos/productDetail.html', context)
