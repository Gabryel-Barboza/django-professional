from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'stock', 'image']

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

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        stock = cleaned_data.get('stock')

        if price and stock and (price * stock) > 100000:
            raise forms.ValidationError(
                'Valor total em estoque (preço × quantidade) excede o limite de R$ 100.000,00'
            )

        return cleaned_data
