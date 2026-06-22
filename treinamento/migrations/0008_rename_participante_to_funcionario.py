from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treinamento', '0007_alter_treinamento_data_realizada'),
    ]

    operations = [
        migrations.RenameField(
            model_name='treinamento',
            old_name='participante',
            new_name='funcionario',
        ),
        migrations.AlterField(
            model_name='treinamento',
            name='funcionario',
            field=models.CharField(max_length=100, verbose_name='Funcionário'),
        ),
    ]
