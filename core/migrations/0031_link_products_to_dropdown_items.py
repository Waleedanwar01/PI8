from django.db import migrations

def forwards(apps, schema_editor):
    from django.utils.text import slugify
    MainPage = apps.get_model('core', 'MainPage')
    DropdownItem = apps.get_model('core', 'DropdownItem')
    InsuranceProduct = apps.get_model('core', 'InsuranceProduct')

    product_names = [
        "Limo Insurance",
        "Livery Insurance",
        "Shuttle Bus Insurance",
        "Non-Medical Insurance",
        "Box Truck Insurance",
        "Taxi Insurance",
    ]

    for name in product_names:
        slug = slugify(name)
        try:
            page = MainPage.objects.get(slug=slug, is_active=True)
        except MainPage.DoesNotExist:
            continue

        product = InsuranceProduct.objects.filter(slug=slug).first()
        if not product:
            continue

        item, _ = DropdownItem.objects.get_or_create(
            main_page=page,
            title=name,
            defaults={
                "order": 0,
                "is_active": True,
                "description": f"Get a {name} quote fast",
                "hero_title": f"Free {name} Quote",
                "hero_subtitle": "Quick coverage options tailored to your business",
                "content": "",
                "meta_title": name,
                "meta_description": f"{name} for vehicles, drivers, and passengers — request a quote today.",
            },
        )

        if not product.dropdown_item_id:
            product.dropdown_item_id = item.id
            product.save(update_fields=["dropdown_item"])

def backwards(apps, schema_editor):
    DropdownItem = apps.get_model('core', 'DropdownItem')
    InsuranceProduct = apps.get_model('core', 'InsuranceProduct')
    from django.utils.text import slugify

    product_names = [
        "Limo Insurance",
        "Livery Insurance",
        "Shuttle Bus Insurance",
        "Non-Medical Insurance",
        "Box Truck Insurance",
        "Taxi Insurance",
    ]

    for name in product_names:
        slug = slugify(name)
        product = InsuranceProduct.objects.filter(slug=slug).first()
        if product and product.dropdown_item_id:
            product.dropdown_item_id = None
            product.save(update_fields=["dropdown_item"])

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0030_remove_faqsubcategory_rewire_items'),
    ]

    operations = [
        migrations.RunPython(forwards, reverse_code=backwards),
    ]
