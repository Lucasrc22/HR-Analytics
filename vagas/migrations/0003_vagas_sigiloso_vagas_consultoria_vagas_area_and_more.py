from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vagas', '0002_vagas_justificativa_vagas_motivo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vagas',
            name='sigiloso',
            field=models.BooleanField(default=False, verbose_name='Sigiloso'),
        ),
        migrations.AddField(
            model_name='vagas',
            name='consultoria',
            field=models.BooleanField(default=False, verbose_name='Consultoria'),
        ),
        migrations.AddField(
            model_name='vagas',
            name='area',
            field=models.CharField(max_length=100, verbose_name='Área'),
        ),
        migrations.AddField(
            model_name='vagas',
            name='quantidade',
            field=models.PositiveIntegerField(verbose_name='Quantidade'),
        ),
    ]
