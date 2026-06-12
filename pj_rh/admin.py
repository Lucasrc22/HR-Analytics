from django.contrib import admin
from pj_rh.models import Prestador


class PrestadorAdmin(admin.ModelAdmin):
    list_display = ["nome_funcionario", "nome_empresa", "setor", "data_admissao", "data_demissao"]
    list_filter = ["nome_empresa", "setor"]
    search_fields = ["nome_funcionario", "nome_empresa", "setor"]
    fieldsets = (
        ("Empresa", {
            "fields": ("nome_empresa", "setor")
        }),
        ("Funcionário", {
            "fields": ("nome_funcionario",)
        }),
        ("Período", {
            "fields": ("data_admissao", "data_demissao")
        }),
    )


admin.site.register(Prestador, PrestadorAdmin)
