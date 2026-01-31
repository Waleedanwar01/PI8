from django.db import migrations

def seed_pages(apps, schema_editor):
    MainPage = apps.get_model("core", "MainPage")

    pages = [
        ("Request a Quote", "request-a-quote"),
        ("Limo Insurance", "limo-insurance"),
        ("Livery Insurance", "livery-insurance"),
        ("Shuttle Bus Insurance", "shuttle-bus-insurance"),
        ("Non-Medical Insurance", "non-medical-insurance"),
        ("Box Truck Insurance", "box-truck-insurance"),
    ]

    for title, slug in pages:
        MainPage.objects.get_or_create(
            slug=slug,
            defaults={
                "title": title,
                "is_active": True,
                "show_in_navbar": False,
                "content": f"<h2>{title}</h2><p>Content for {title} goes here. You can edit this in the Admin panel.</p>"
            }
        )

def reverse_seed(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_mainpage_show_in_navbar'),
    ]

    operations = [
        migrations.RunPython(seed_pages, reverse_seed),
    ]
