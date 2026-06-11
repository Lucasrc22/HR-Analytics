from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='dat_afast_func_acidte',
            field=models.DateField(verbose_name='Data de afastamento'),
        ),
    ]
