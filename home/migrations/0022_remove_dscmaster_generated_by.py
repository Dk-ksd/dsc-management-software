# Generated by Django 5.1.6 on 2025-04-15 02:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_alter_usagelogs_form_id_alter_usagelogs_platform_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dscmaster',
            name='generated_by',
        ),
    ]
