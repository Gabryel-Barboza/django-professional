from django.contrib import admin

from .forms import ProductForm
from .models import Category, Product


# ─── ProductAdmin ────────────────────────────────────────────────────
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm

    list_display = ('name', 'category', 'price', 'stock', 'get_short_id')
    list_filter = ('category', 'created_at')

    search_fields = ('name', 'category__name', 'uuid')

    list_editable = ('price', 'stock')
    list_select_related = ('category',)

    fields = ('name', 'price', 'stock', 'category', 'image', 'created_at')

    readonly_fields = ('created_at',)

    def get_short_id(self, obj):
        return str(obj.uuid)[:8]

    get_short_id.short_description = 'ID Reduzido'


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


# ─── CategoryAdmin ───────────────────────────────────────────────────
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductInline]
