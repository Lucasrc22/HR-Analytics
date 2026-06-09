from django.contrib import admin
from legal_person.models import Prestador


class PrestadorAdmin(admin.ModelAdmin):
    list_display = ["nome_funcionario", "matricula", "nome_empresa", "setor", "data_admissao", "data_demissao"]
    list_filter = ["nome_empresa", "setor"]
    search_fields = ["nome_funcionario", "matricula", "nome_empresa", "setor"]
    fieldsets = (
        ("Empresa", {
            "fields": ("nome_empresa", "setor")
        }),
        ("Funcionário", {
            "fields": ("matricula", "nome_funcionario")
        }),
        ("Período", {
            "fields": ("data_admissao", "data_demissao")
        }),
    )


admin.site.register(Prestador, PrestadorAdmin)
