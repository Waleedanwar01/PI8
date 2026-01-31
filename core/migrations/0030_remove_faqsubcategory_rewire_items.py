from django.db import migrations, models

def forwards(apps, schema_editor):
    FAQItem = apps.get_model('core', 'FAQItem')
    try:
        FAQSubCategory = apps.get_model('core', 'FAQSubCategory')
    except LookupError:
        FAQSubCategory = None
    if FAQSubCategory:
        for item in FAQItem.objects.all():
            # Copy category from the item's subcategory
            if getattr(item, 'subcategory_id', None):
                subcat = FAQSubCategory.objects.filter(pk=item.subcategory_id).only('category_id').first()
                if subcat:
                    item.category_id = subcat.category_id
                    item.save(update_fields=['category_id'])

def noop(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0029_seed_insurance_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqitem',
            name='category',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='items', to='core.faqcategory', null=True),
        ),
        migrations.RunPython(forwards, reverse_code=noop),
        migrations.AlterField(
            model_name='faqitem',
            name='category',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='items', to='core.faqcategory'),
        ),
        migrations.RemoveField(
            model_name='faqitem',
            name='subcategory',
        ),
        migrations.DeleteModel(
            name='FAQSubCategory',
        ),
    ]
