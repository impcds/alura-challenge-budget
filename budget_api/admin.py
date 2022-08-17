from django.contrib import admin
from budget_api.models import Despesa, Receita


class DespesaAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'valor', 'data')


class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'valor', 'data')


admin.site.register(Despesa, DespesaAdmin)
admin.site.register(Receita, ReceitaAdmin)
