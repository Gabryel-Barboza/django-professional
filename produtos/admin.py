"""
ADMIN — Interface Administrativa do Django

┌──────────────────────────────────────────────────────────────────────┐
│ CONCEITOS-CHAVE:                                                     │
│                                                                      │
│ @admin.register(Model) vs admin.site.register(Model, ModelAdmin)     │
│   Decorator é mais limpo e mantém registro perto da definição.       │
│                                                                      │
│ list_display      → colunas exibidas na listagem                     │
│ list_filter       → filtros laterais (ForeignKey e Date funcionam    │
│                     melhor por já terem widgets apropriados)         │
│ search_fields     → campos pesquisados na barra de busca             │
│                     (usa __icontains automaticamente)                │
│ list_editable     → editar campos sem entrar no formulário           │
│ list_select_related → JOIN antecipado para evitar N+1 no admin       │
│ prepopulated_fields → preenche slug automaticamente via JavaScript   │
│                                                                      │
│ INLINES: editar modelos relacionados na MESMA tela do pai.           │
│   TabularInline  → layout em tabela (mais compacto)                  │
│   StackedInline  → layout em formulário vertical (mais espaço)       │
│   extra: quantos forms em branco mostrar além dos existentes         │
│                                                                      │
│ N+1 no admin: se o list_display tem uma FK, o Django carrega cada    │
│ registro relacionado com uma query separada. list_select_related     │
│ resolve isso com um JOIN na query principal.                         │
└──────────────────────────────────────────────────────────────────────┘
"""

from django.contrib import admin

from .models import Category, Product


# ─── ProductAdmin ────────────────────────────────────────────────────
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'get_short_id')
    list_filter = ('category', 'created_at')
    search_fields = ('category', 'uuid')
    list_editable = ('price', 'stock')
    list_select_related = ('category',)  # ← resolve N+1 da FK category

    # Método customizado: qualquer método do ModelAdmin que receba (self, obj)
    # pode ser usado como coluna em list_display.
    # obj é a instância do modelo (Product).
    def get_short_id(self, obj):
        return str(obj.id)[:8]  # mostra só os 8 primeiros caracteres do UUID

    # short_description: legenda da coluna no admin (em português)
    get_short_id.short_description = 'ID Reduzido'


# ─── ProductInline ───────────────────────────────────────────────────
# Inline = editar produtos dentro da página de edição da categoria.
# Útil quando você quer criar vários produtos de uma vez para uma categoria.
class ProductInline(admin.TabularInline):
    model = Product
    extra = 1  # número de linhas em branco após os registros existentes


# ─── CategoryAdmin ───────────────────────────────────────────────────
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductInline]  # ← edita produtos na tela da categoria
