# Generated by Django 5.1.4 on 2025-02-23 14:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_inout_direction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dscmaster',
            name='dsc_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.dsc_class'),
        ),
        migrations.AlterField(
            model_name='dscmaster',
            name='email_id',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='dscmaster',
            name='issuing_auth',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.issuingauth'),
        ),
        migrations.AlterField(
            model_name='dscmaster',
            name='type',
            field=models.CharField(blank=True, choices=[('Organization', 'Organization'), ('Individual', 'Individual')], max_length=50, null=True),
        ),
    ]
