from django.db import models


class CAT(models.Model):

    EMPRESA = [
        ('AGRO INDUSTRIAL TABU S/A', 'AGRO INDUSTRIAL TABU S/A'),
        ('INSOLITO HOTEL LTDA', 'INSOLITO HOTEL LTDA'),
        ('GALACTUS DO BRASIL', 'GALACTUS DO BRASIL'),
        ('TRANCOSO BIO RISORT AGROPECUARIA LTDA', 'TRANCOSO BIO RISORT AGROPECUARIA LTDA'),
        ('MEG DISTRIBUIDORA DE COMBUSTIVEIS LTDA', 'MEG DISTRIBUIDORA DE COMBUSTIVEIS LTDA'),
        ('JUBARTE CONCEITO','JUBARTE CONCEITO')
    ]
    
    nom_empresa = models.CharField("Nome da empresa", max_length=40, default="", choices=EMPRESA)
    nom_funcionario = models.CharField("Nome do funcionário", max_length=60, default="")
    setor = models.CharField("Setor", max_length=60, default="")
    acidente = models.CharField("Acidente", max_length=100, default="")
    dat_afast_func_acidte = models.DateField("Data do acidente", default=None)

    class Meta:
        
        db_table = "cat_rh"

    def __str__(self):
        return f"CAT {self.matricula} - {self.nom_funcionario}"
