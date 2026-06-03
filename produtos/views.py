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
│                                                                      │
│ FLASH MESSAGES (Sistema de Mensagens Nativo):                       │
│   from django.contrib import messages                               │
│   messages.success(request, 'texto')  → alerta verde (success)     │
│   messages.warning(request, 'texto') → alerta amarelo (warning)    │
│   messages.error(request, 'texto')   → alerta vermelho (error)     │
│   messages.info(request, 'texto')    → alerta azul (info)          │
│                                                                      │
│   As mensagens são armazenadas na sessão e exibidas UMA ÚNICA vez   │
│   no template (efêmeras — somem após o primeiro render).            │
│   No template: {% for message in messages %}...{{ message }}...     │
└──────────────────────────────────────────────────────────────────────┘
"""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from .forms import ProductForm
from .models import Product


def list_products(request):
    products = Product.objects.all()
    context = {'products_list': products, 'title': 'Nossa Vitrine'}
    return render(request, 'produtos/productsList.html', context)


def get_product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'produtos/productDetail.html', context)


def create_product_view(request):
    if request.method == 'POST':
        # Passamos os dados textuais (POST) e os arquivos/imagens (FILES) para o formulário
        form = ProductForm(request.POST, request.FILES)

        # is_valid() roda: validação de tipo → clean_<campo>() → clean()
        if form.is_valid():
            form.save()

            # ─── FLASH MESSAGE ───────────────────────────────────────
            # messages.success() armazena na sessão uma mensagem que
            # será exibida na PRÓXIMA requisição (após o redirect).
            # A mensagem some depois de renderizada uma vez.
            messages.success(request, 'Produto cadastrado com sucesso!')

            return redirect('products_list')
        else:
            # Se o formulário for inválido, avisa o usuário
            messages.error(
                request,
                'Erro ao cadastrar produto. Verifique os dados e tente novamente.',
            )
    else:
        form = ProductForm()

    return render(request, 'produtos/createProduct.html', {'form': form})


# ─── Class-Based View (CBV) — ListView ──────────────────────────────
# Vantagens sobre FBV: menos código boilerplate, métodos específicos
# (get_queryset, get_context_data), reuso via mixins.
# Desvantagem: menos explícito, curva de aprendizado maior.
class ProductsListView(ListView):
    model = Product
    template_name = 'produtos/productsList.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Sobrescreve para adicionar select_related e evitar N+1."""
        return Product.objects.select_related('category').all()

    def get_context_data(self, **kwargs):
        """Sobrescreve para injetar dados extras no contexto."""
        from .models import Category

        context = super().get_context_data(**kwargs)
        context['total_categories'] = Category.objects.count()
        context['title'] = 'Nossa Vitrine (CBV)'
        return context
