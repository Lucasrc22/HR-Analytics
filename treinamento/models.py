from django.db import models

class Treinamento(models.Model):
    area = models.CharField("Área",max_length=100, null=False, blank=False)
    treinamento = models.CharField("Treinamento",max_length=100, null=False, blank=False)
    participante = models.IntegerField("Participante", null=False, blank=False)
    carga_horaria = models.IntegerField("Carga Horária", null=False, blank=False)
    programado = models.BooleanField("Programado", default=False)
    realizado = models.BooleanField("Realizado", default=False)
    reprogramado = models.BooleanField("Reprogramado", default=False)
    cancelado = models.BooleanField("Cancelado", default=False)
    nenhuma_alternativa = models.BooleanField("Nenhuma Alternativa", default=False)
    sem_data_prevista = models.BooleanField("Sem Data Prevista", default=False)
    nao_realizado = models.BooleanField("Não Realizado", default=False)

    def __str__(self):
        return f"{self.area} - {self.treinamento} ({self.participante} participantes)"
