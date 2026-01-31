from django.db import migrations

def backfill_dropdownitem_slugs(apps, schema_editor):
    DropdownItem = apps.get_model('core', 'DropdownItem')
    items = DropdownItem.objects.filter(slug__isnull=True) | DropdownItem.objects.filter(slug='')
    for item in items:
        item.save()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0032_insuranceproduct_description_and_more'),
    ]
    operations = [
        migrations.RunPython(backfill_dropdownitem_slugs, migrations.RunPython.noop),
    ]
