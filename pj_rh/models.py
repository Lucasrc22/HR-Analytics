from django.db import models


class Prestador(models.Model):
    EMPRESA = [
        ('AGRO INDUSTRIAL TABU S/A', 'AGRO INDUSTRIAL TABU S/A'),
        ('INSOLITO HOTEL LTDA', 'INSOLITO HOTEL LTDA'),
        ('GALACTUS DO BRASIL', 'GALACTUS DO BRASIL'),
        ('TRANCOSO BIO RISORT AGROPECUARIA LTDA', 'TRANCOSO BIO RISORT AGROPECUARIA LTDA'),
        ('MEG DISTRIBUIDORA DE COMBUSTIVEIS LTDA', 'MEG DISTRIBUIDORA DE COMBUSTIVEIS LTDA'),
        ('JUBARTE CONCEITO','JUBARTE CONCEITO')
    ]

    
    nome_empresa = models.CharField("Nome da empresa", max_length=200, choices=EMPRESA)
    nome_funcionario = models.CharField("Nome do funcionário", max_length=150)
    setor = models.CharField("Setor", max_length=120)
    data_admissao = models.DateField("Data de admissão")
    data_demissao = models.DateField("Data de demissão", null=True, blank=True)

    class Meta:
        verbose_name = "Prestador"
        verbose_name_plural = "Prestadores"
        ordering = ["nome_empresa", "nome_funcionario"]

    def __str__(self):
        return f"{self.nome_funcionario} — {self.nome_empresa}"
