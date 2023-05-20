# Generated by Django 4.1.7 on 2023-05-18 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0005_alter_saleshistory_hospital_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleshistory',
            name='status',
            field=models.CharField(choices=[('A', 'ACT'), ('B', 'BEST_CASE'), ('P', 'PIPELINE'), ('O', 'OPP'), ('F', 'FUNNEL')], default='A', max_length=10),
        ),
    ]