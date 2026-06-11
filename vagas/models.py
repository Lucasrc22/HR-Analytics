from django.db import models


class Vagas(models.Model):

    STATUS_CHOICES = [
        ('Aberta', 'Aberta'),
        ('Fechada', 'Fechada')
    ]

    EMPRESA = [
        ('AGRO INDUSTRIAL TABU S/A', 'AGRO INDUSTRIAL TABU S/A'),
        ('INSOLITO HOTEL LTDA', 'INSOLITO HOTEL LTDA'),
        ('GALACTUS DO BRASIL', 'GALACTUS DO BRASIL'),
        ('TRANCOSO BIO RISORT AGROPECUARIA LTDA', 'TRANCOSO BIO RISORT AGROPECUARIA LTDA'),
        ('MEG DISTRIBUIDORA DE COMBUSTIVEIS LTDA', 'MEG DISTRIBUIDORA DE COMBUSTIVEIS LTDA'),
        ('JUBARTE CONCEITO','JUBARTE CONCEITO')
    ]


    empresa = models.CharField("Empresa",max_length=100, null=False, blank=False, choices=EMPRESA)
    tipo_vaga = models.CharField("Tipo de Vaga",max_length=100, null=False, blank=False)
    data_abertura = models.DateField("Data de Abertura", null=False, blank=False)
    data_fechamento = models.DateField("Data de Fechamento", null=True, blank=True)
    cargo = models.CharField("Cargo",max_length=100, null=False, blank=False)
    status = models.CharField("Status",max_length=100, null=False, blank=False, choices=STATUS_CHOICES)
    motivo = models.TextField("Motivo", null=True, blank=True)
    justificativa = models.TextField("Justificativa", null=True, blank=True)
    nome_candidato = models.CharField("Nome do Candidato", max_length=100, null=True, blank=True)
    previsao_admissao = models.DateField("Previsão de Admissão", null=True, blank=True)
    observacoes = models.TextField("Observações", null=True, blank=True)
    
    def __str__(self):
        return f"{self.empresa} - {self.cargo} ({self.status})"
