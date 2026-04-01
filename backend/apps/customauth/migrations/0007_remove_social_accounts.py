from django.db import migrations

def remove_social_accounts(apps, schema_editor):
    # This will be handled by Django's natural migration
    pass

def reverse_remove_social_accounts(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('customauth', '0006_customuser_phone_number'),  # Replace with your latest migration
    ]

    operations = [
        migrations.RunPython(remove_social_accounts, reverse_remove_social_accounts),
    ]