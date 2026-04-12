from django.contrib import admin

from .models import Category, Product

# Register your models here.

# Registro direto
"""admin.site.register(
    (
        Product,
        Category,
    )
)"""


# Registro com configuração do modelo de admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Colunas que aparecerão na tabela
    list_display = ('name', 'category', 'price', 'stock', 'get_short_id')

    # Adiciona uma barra lateral de filtros (campos ForeignKey ou Date funcionam melhor)
    list_filter = ('category', 'created_at')

    # Adiciona uma barra de pesquisa (pesquisa nos campos informados)
    search_fields = ('category', 'uuid')

    # Permite editar campos diretamente na lista (sem entrar no produto)
    list_editable = ('price', 'stock')

    # Evita problema de N + 1 ao selecionar todos os elementos relacionados em uma consulta.
    list_select_related = ('category',)

    # Método customizado para exibir apenas o começo do UUID
    def get_short_id(self, obj):
        return str(obj.id)[:8]

    get_short_id.short_description = 'ID Reduzido'


# Inlines ou campos para adição rápida de modelos em outros modelos.
class ProductInline(admin.TabularInline):
    model = Product
    extra = 1  # Campos vazios após último elemento.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    # Popular campos com valores do modelo.
    prepopulated_fields = {'slug': ('name',)}

    inlines = [ProductInline]  # Adicionando campo de inlines
