"""
ADMIN DO USERS — Custom User Model no Admin

┌──────────────────────────────────────────────────────────────────────┐
│ UserAdmin (django.contrib.auth.admin.UserAdmin)                      │
│                                                                      │
│ Diferente de um ModelAdmin comum, o UserAdmin já trata:              │
│   - Formulário de CRIAÇÃO com password1/password2 (confirmação)      │
│   - Formulário de EDIÇÃO exibindo o HASH da senha (nunca o texto)    │
│   - Campos de permissão (groups, user_permissions)                   │
│                                                                      │
│ ESTRUTURA:                                                           │
│   fieldsets       → agrupamento de campos no formulário de EDIÇÃO    │
│   add_fieldsets   → agrupamento de campos no formulário de CRIAÇÃO   │
│   list_display    → colunas na listagem                              │
│   search_fields   → campos pesquisáveis                              │
│   ordering        → ordenação padrão                                 │
│                                                                      │
│ FORMULÁRIOS PERSONALIZADOS                                           │
│   CustomUserCreationForm: herda UserCreationForm e aponta model=User │
│     → Garante que os campos extras (cpf) apareçam na criação         │
│   CustomUserChangeForm: herda UserChangeForm e aponta model=User     │
│     → Garante que cpf seja editável no formulário de edição          │
│                                                                      │
│ O método save_model() do UserAdmin criptografa a senha               │
│ automaticamente ao criar/alterar. Não precisa reimplementar.         │
└──────────────────────────────────────────────────────────────────────┘
"""

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'username', 'cpf')
    search_fields = ('email', 'username', 'cpf')
    ordering = ('email',)

    # fieldsets: agrupa campos no formulário de EDIÇÃO de usuário
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('email', 'cpf')}),
        (
            'Permissões',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        ('Datas', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        'Novo Usuário',
        {'fields': ('username', 'email', 'password1', 'password2')},
    )
