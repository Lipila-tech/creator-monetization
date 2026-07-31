# Generated manual data migration to convert existing payments from 'pawapay' to 'lipila'
from django.db import migrations


def forwards_func(apps, schema_editor):
    Payment = apps.get_model('payments', 'Payment')
    qs = Payment.objects.filter(provider='pawapay')
    for p in qs:
        p.provider = 'lipila'
        p.provider_metadata = p.provider_metadata or {}
        p.provider_metadata['migrated_from'] = 'pawapay'
        p.save(update_fields=['provider', 'provider_metadata'])


def reverse_func(apps, schema_editor):
    Payment = apps.get_model('payments', 'Payment')
    qs = Payment.objects.filter(provider='lipila', provider_metadata__contains={'migrated_from': 'pawapay'})
    for p in qs:
        p.provider = 'pawapay'
        meta = p.provider_metadata or {}
        meta.pop('migrated_from', None)
        p.provider_metadata = meta
        p.save(update_fields=['provider', 'provider_metadata'])


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
