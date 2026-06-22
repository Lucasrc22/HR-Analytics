from django.contrib import admin
from .models import Treinamento


@admin.register(Treinamento)
class TreinamentoAdmin(admin.ModelAdmin):
    list_display = (
        'area', 'treinamento', 'funcionario', 'empresa', 'carga_horaria',
        'data_inicio', 'data_fim_planejada', 'data_realizada',
        'programado', 'realizado', 'reprogramado', 'cancelado',
        'nenhuma_alternativa', 'sem_data_prevista', 'nao_realizado',
    )
    list_filter = (
        'area', 'empresa', 'programado', 'realizado', 'reprogramado',
        'cancelado', 'nenhuma_alternativa', 'sem_data_prevista', 'nao_realizado',
    )
    search_fields = ('area', 'treinamento', 'funcionario', 'empresa')
    list_per_page = 25
    fieldsets = (
        (None, {
            'fields': ('area', 'treinamento', 'funcionario', 'empresa', 'carga_horaria'),
        }),
        ('Período', {
            'fields': ('data_inicio','data_fim_planejada', 'data_realizada'),
        }),
        ('Status', {
            'fields': (
                'programado', 'realizado', 'reprogramado', 'cancelado',
                'nenhuma_alternativa', 'sem_data_prevista', 'nao_realizado',
            ),
        }),
    )

