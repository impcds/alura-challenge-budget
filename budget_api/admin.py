from django.contrib import admin
from budget_api.models import Despesa, Receita


class DespesaAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'valor', 'data', 'usuario')
    search_fields = ('descricao', )


class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'valor', 'data')
    search_fields = ('descricao', )


admin.site.register(Despesa, DespesaAdmin)
admin.site.register(Receita, ReceitaAdmin)
