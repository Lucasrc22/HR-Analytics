from django.contrib import admin
from .models import CAT


@admin.register(CAT)
class CATAdmin(admin.ModelAdmin):
    list_display = ["id", "nom_empresa", "matricula", "nom_funcionario", "setor", "dat_afast_func_acidte"]
    list_filter = ["nom_empresa", "setor", "dat_afast_func_acidte"]
    search_fields = ["nom_funcionario", "matricula", "nom_empresa", "setor"]
