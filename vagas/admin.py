from django.contrib import admin
from .models import Vagas


@admin.register(Vagas)
class VagasAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'cargo', 'area', 'tipo_vaga', 'quantidade', 'data_abertura', 'data_fechamento', 'status', 'sigiloso', 'consultoria')
    list_filter = ('empresa', 'status', 'tipo_vaga', 'area', 'sigiloso', 'consultoria')
    search_fields = ('cargo', 'tipo_vaga', 'area')
    list_per_page = 25
    fieldsets = (
        (None, {
            'fields': ('empresa', 'cargo', 'area', 'tipo_vaga', 'quantidade', 'status', 'sigiloso', 'consultoria'),
        }),
        ('Datas', {
            'fields': ('data_abertura', 'data_fechamento'),
        }),
        ('Fechamento / Candidato', {
            'fields': ('motivo', 'justificativa', 'nome_candidato', 'previsao_admissao', 'observacoes'),
        }),
    )
