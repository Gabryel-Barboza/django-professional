"""
FORMULÁRIOS — ModelForms e Validação

┌──────────────────────────────────────────────────────────────────────┐
│ Form vs ModelForm                                                    │
│   Form         → genérico, não vinculado a modelo (ex: login, busca) │
│   ModelForm    → vinculado a um modelo, gera campos automaticamente  │
│                                                                      │
│ CAMPOS:                                                              │
│   fields = ['campo1', 'campo2'] → whitelist (MAIS SEGURO)           │
│   exclude = ['campo1']          → blacklist                         │
│   Sempre prefira fields (se esquecer de excluir um campo sensível   │
│   como is_staff, ele aparece e o usuário pode se auto-promover).    │
│                                                                      │
│ VALIDAÇÃO — Fluxo completo ao chamar form.is_valid():                │
│   1. Validação automática do Django (tipo, required, max_length...)  │
│   2. clean_<campo>()  → para CADA campo que definiu o método        │
│      → valida UM campo isoladamente                                 │
│      → retorna o valor validado (ou raise ValidationError)          │
│   3. clean()          → validação CRUZADA (multi-campos)            │
│      → self.cleaned_data tem TODOS os campos já validados           │
│      → DEVE retornar cleaned_data no final                          │
│                                                                      │
│ INJEÇÃO NO ADMIN:                                                    │
│   Em admin.py, basta definir: form = ProductForm                    │
│   O admin passa a usar SEU formulário em vez do gerado por padrão.  │
└──────────────────────────────────────────────────────────────────────┘
"""

from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Whitelist de campos — mais seguro que exclude
        fields = ['category', 'name', 'price', 'stock', 'image']

    # ─── clean_<campo> — Validação INDIVIDUAL ─────────────────────────
    # O Django chama automaticamente clean_price() após validar o tipo
    # do campo (se é Decimal, se é required, etc.).
    # self.cleaned_data já contém o valor convertido.
    # Se não retornar o valor, o campo fica None no banco.

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError(
                'O preço do produto não pode ser nulo ou negativo!'
            )
        return price

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock <= 0:
            raise forms.ValidationError('O estoque não pode ser nulo!')
        elif stock > 999:
            raise forms.ValidationError(
                'O limite de produtos em estoque permitidos é: 999'
            )
        return stock

    # ─── clean() — Validação MULTI-CAMPOS ────────────────────────────
    # Diferente de clean_<campo>(), aqui temos ACESSO A TODOS os campos
    # já validados individualmente. Ideal para regras de negócio que
    # CRUZAM informações (ex: data_inicio < data_fim, preço * quantidade).
    #
    # ⚠️ Sempre chamar super().clean() no início e retornar cleaned_data.

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        stock = cleaned_data.get('stock')

        if price and stock and (price * stock) > 100000:
            raise forms.ValidationError(
                'Valor total em estoque (preço × quantidade) excede o limite de R$ 100.000,00'
            )

        return cleaned_data
