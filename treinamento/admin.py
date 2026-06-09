from django.contrib import admin
from .models import Treinamento


@admin.register(Treinamento)
class TreinamentoAdmin(admin.ModelAdmin):
    list_display = (
        'area', 'treinamento', 'participante', 'carga_horaria',
        'programado', 'realizado', 'reprogramado', 'cancelado',
        'nenhuma_alternativa', 'sem_data_prevista', 'nao_realizado',
    )
    list_filter = (
        'area', 'programado', 'realizado', 'reprogramado',
        'cancelado', 'nenhuma_alternativa', 'sem_data_prevista', 'nao_realizado',
    )
    search_fields = ('area', 'treinamento')
    list_per_page = 25
    fieldsets = (
        (None, {
            'fields': ('area', 'treinamento', 'participante', 'carga_horaria'),
        }),
        ('Status', {
            'fields': (
                'programado', 'realizado', 'reprogramado', 'cancelado',
                'nenhuma_alternativa', 'sem_data_prevista', 'nao_realizado',
            ),
        }),
    )

