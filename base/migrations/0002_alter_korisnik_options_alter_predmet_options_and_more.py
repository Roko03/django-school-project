# Generated by Django 5.0.6 on 2024-05-28 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='korisnik',
            options={'verbose_name_plural': 'Korisnici'},
        ),
        migrations.AlterModelOptions(
            name='predmet',
            options={'verbose_name_plural': 'Predmeti'},
        ),
        migrations.AlterField(
            model_name='korisnik',
            name='status',
            field=models.CharField(blank=True, choices=[('none', 'None'), ('izv', 'izvanredni student'), ('red', 'redovni student')], max_length=50),
        ),
    ]
