from django.db import migrations, models

def create_initial_templates(apps, schema_editor):
    EmailTemplate = apps.get_model('home', 'EmailTemplate')
    
    EmailTemplate.objects.get_or_create(
        template_type='expired',
        defaults={
            'subject': '⚠️ Your DSC ({dsc_number}) Has Expired!',
            'body': """Dear {full_name},

Your Digital Signature Certificate ({dsc_number}) expired on {expiry_date}.
Please renew it as soon as possible to continue using it.

Thank you,
DSC Management Team"""
        }
    )
    
    EmailTemplate.objects.get_or_create(
        template_type='expiring',
        defaults={
            'subject': '⏳ Your DSC ({dsc_number}) Will Expire Soon!',
            'body': """Dear {full_name},

Your Digital Signature Certificate ({dsc_number}) is set to expire on {expiry_date}.
Please ensure you renew it before the expiry date.

Thank you,
DSC Management Team"""
        }
    )

class Migration(migrations.Migration):
    dependencies = [
        ('home', '0019_alter_dscextrafield_field_name'),  # This is correct
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_type', models.CharField(choices=[('expired', 'Expired DSC Notification'), ('expiring', 'Expiring Soon DSC Notification')], max_length=20, unique=True)),
                ('subject', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RunPython(create_initial_templates),
    ]