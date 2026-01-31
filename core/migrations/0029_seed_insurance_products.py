from django.db import migrations

def seed_products(apps, schema_editor):
    from django.utils.text import slugify
    InsuranceProduct = apps.get_model('core', 'InsuranceProduct')
    InsuranceCoverageType = apps.get_model('core', 'InsuranceCoverageType')
    FAQCategory = apps.get_model('core', 'FAQCategory')

    coverage_names = [
        "Auto Liability",
        "General Liability",
        "Physical Damage",
        "Cargo",
        "Workers Compensation",
        "Medical Payments",
        "UM/UIM",
        "Hired/Non-Owned Auto",
    ]
    coverages = []
    for name in coverage_names:
        c, _ = InsuranceCoverageType.objects.get_or_create(name=name, defaults={"slug": slugify(name), "is_active": True})
        coverages.append(c)

    products = [
        "Taxi Insurance",
        "Limo Insurance",
        "Livery Insurance",
        "Shuttle Bus Insurance",
        "Non-Medical Insurance",
        "Box Truck Insurance",
    ]

    for name in products:
        p, _ = InsuranceProduct.objects.get_or_create(
            name=name,
            defaults={"slug": slugify(name), "is_active": True, "order": 0},
        )
        p.coverages.set(coverages)
        try:
            cat = FAQCategory.objects.get(name=name)
            cat.insurance_product_id = p.id
            cat.save(update_fields=["insurance_product"])
        except FAQCategory.DoesNotExist:
            pass

def unseed_products(apps, schema_editor):
    InsuranceProduct = apps.get_model('core', 'InsuranceProduct')
    FAQCategory = apps.get_model('core', 'FAQCategory')
    names = [
        "Taxi Insurance",
        "Limo Insurance",
        "Livery Insurance",
        "Shuttle Bus Insurance",
        "Non-Medical Insurance",
        "Box Truck Insurance",
    ]
    InsuranceProduct.objects.filter(name__in=names).delete()
    FAQCategory.objects.filter(name__in=names).update(insurance_product=None)

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0028_seed_initial_insurance_faq_categories'),
    ]

    operations = [
        migrations.RunPython(seed_products, reverse_code=unseed_products),
    ]
