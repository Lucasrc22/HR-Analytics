from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treinamento', '0008_rename_participante_to_funcionario'),
    ]

    operations = [
        migrations.AddField(
            model_name='treinamento',
            name='empresa',
            field=models.CharField(
                default='',
                max_length=100,
                verbose_name='Empresa',
                choices=[
                    ('AGRO INDUSTRIAL TABU S/A', 'AGRO INDUSTRIAL TABU S/A'),
                    ('INSOLITO HOTEL LTDA', 'INSOLITO HOTEL LTDA'),
                    ('GALACTUS DO BRASIL', 'GALACTUS DO BRASIL'),
                    ('TRANCOSO BIO RISORT AGROPECUARIA LTDA', 'TRANCOSO BIO RISORT AGROPECUARIA LTDA'),
                    ('MEG DISTRIBUIDORA DE COMBUSTIVEIS LTDA', 'MEG DISTRIBUIDORA DE COMBUSTIVEIS LTDA'),
                    ('JUBARTE CONCEITO', 'JUBARTE CONCEITO'),
                ],
            ),
            preserve_default=False,
        ),
    ]
