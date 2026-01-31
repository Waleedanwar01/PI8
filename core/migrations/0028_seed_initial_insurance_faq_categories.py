from django.db import migrations

def seed_data(apps, schema_editor):
    from django.utils.text import slugify
    InsuranceCoverageType = apps.get_model('core', 'InsuranceCoverageType')
    FAQCategory = apps.get_model('core', 'FAQCategory')
    FAQSubCategory = apps.get_model('core', 'FAQSubCategory')
    FAQItem = apps.get_model('core', 'FAQItem')

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

    categories = [
        "Limo Insurance",
        "Livery Insurance",
        "Shuttle Bus Insurance",
        "Non-Medical Insurance",
        "Box Truck Insurance",
    ]

    for cat_name in categories:
        cat, _ = FAQCategory.objects.get_or_create(
            name=cat_name,
            defaults={
                "slug": slugify(cat_name),
                "is_active": True,
                "order": 0,
            },
        )
        cat.coverages.set(coverages)

        sub_general, _ = FAQSubCategory.objects.get_or_create(
            category=cat,
            name="General",
            defaults={"slug": "general", "is_active": True, "order": 0},
        )
        sub_coverage, _ = FAQSubCategory.objects.get_or_create(
            category=cat,
            name="Coverage",
            defaults={"slug": "coverage", "is_active": True, "order": 1},
        )

        FAQItem.objects.get_or_create(
            subcategory=sub_general,
            question="How do I get a quote?",
            defaults={
                "answer": "Submit the quote form on the category page with your business details.",
                "is_active": True,
                "order": 0,
            },
        )
        FAQItem.objects.get_or_create(
            subcategory=sub_general,
            question="What documents are required?",
            defaults={
                "answer": "Typically driver list, vehicle list, and loss runs if applicable.",
                "is_active": True,
                "order": 1,
            },
        )
        FAQItem.objects.get_or_create(
            subcategory=sub_coverage,
            question="Which coverages are included?",
            defaults={
                "answer": "Common coverages include Auto Liability, General Liability, Physical Damage, Cargo, and Workers Compensation.",
                "is_active": True,
                "order": 0,
            },
        )

def unseed_data(apps, schema_editor):
    FAQCategory = apps.get_model('core', 'FAQCategory')
    FAQSubCategory = apps.get_model('core', 'FAQSubCategory')
    FAQItem = apps.get_model('core', 'FAQItem')
    categories = FAQCategory.objects.filter(name__in=[
        "Limo Insurance",
        "Livery Insurance",
        "Shuttle Bus Insurance",
        "Non-Medical Insurance",
        "Box Truck Insurance",
    ])
    FAQItem.objects.filter(subcategory__category__in=categories).delete()
    FAQSubCategory.objects.filter(category__in=categories).delete()
    categories.delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0027_faqcategory_coverages_faqcategory_dropdown_item'),
    ]

    operations = [
        migrations.RunPython(seed_data, reverse_code=unseed_data),
    ]
