# Generated by Django 5.1.6 on 2025-03-05 14:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articulos', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('monto_total', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('reposicion', models.BooleanField(default=False)),
                ('observacion', models.TextField(blank=True, null=True)),
                ('articulo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='articulos.articulorsf')),
            ],
        ),
    ]
