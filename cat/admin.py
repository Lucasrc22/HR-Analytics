from django.contrib import admin
from .models import CAT


@admin.register(CAT)
class CATAdmin(admin.ModelAdmin):
    list_display = ["id", "nom_empresa", "nom_funcionario", "setor", "acidente", "dat_afast_func_acidte"]
    list_filter = ["nom_empresa", "setor", "dat_afast_func_acidte"]
    search_fields = ["nom_funcionario", "nom_empresa", "setor"]
