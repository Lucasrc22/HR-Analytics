from django.contrib import admin
from .models import Vagas


@admin.register(Vagas)
class VagasAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'cargo', 'tipo_vaga', 'data_abertura', 'data_fechamento', 'status')
    list_filter = ('empresa', 'status', 'tipo_vaga')
    search_fields = ('cargo', 'tipo_vaga')
    list_per_page = 25
    fieldsets = (
        (None, {
            'fields': ('empresa', 'cargo', 'tipo_vaga', 'status'),
        }),
        ('Datas', {
            'fields': ('data_abertura', 'data_fechamento'),
        }),
        ('Fechamento / Candidato', {
            'fields': ('motivo', 'justificativa', 'nome_candidato', 'previsao_admissao', 'observacoes'),
        }),
    )
