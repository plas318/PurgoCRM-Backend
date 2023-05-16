# Generated by Django 4.1.7 on 2023-05-13 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_alter_doctor_graduate_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, auto_now=True)),
                ('history_id', models.IntegerField()),
                ('content', models.TextField()),
                ('status', models.SmallIntegerField(choices=[(1, 'ACT'), (2, 'BEST_CASE'), (3, 'PIPELINE'), (4, 'OPP')], default='ACT')),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.hospital')),
            ],
            options={
                'verbose_name': 'History',
            },
        ),
    ]