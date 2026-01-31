from django.db import migrations
from django.utils.text import slugify


def seed_navigation(apps, schema_editor):
    MainPage = apps.get_model("core", "MainPage")
    DropdownItem = apps.get_model("core", "DropdownItem")

    pages = [
        {
            "title": "Prospective Customers",
            "order": 10,
            "url": "",
            "items": [
                {"title": "Request a Quote", "order": 10, "url": "#"},
                {"title": "Sales & Support", "order": 20, "url": "#"},
                {"title": "Definitions", "order": 30, "url": "#"},
                {"title": "Upload File", "order": 40, "url": "#"},
            ],
        },
        {
            "title": "Existing Customers",
            "order": 20,
            "url": "",
            "items": [
                {"title": "Issue Certificate", "order": 10, "url": "#"},
                {"title": "Review Policy", "order": 20, "url": "#"},
                {"title": "Pay Bill", "order": 30, "url": "#"},
                {"title": "Add/Remove Vehicle", "order": 40, "url": "#"},
            ],
        },
        {
            "title": "About Us",
            "order": 30,
            "url": "",
            "items": [
                {"title": "Our Company", "order": 10, "url": "#"},
                {"title": "Our Team", "order": 20, "url": "#"},
                {"title": "Careers", "order": 30, "url": "#"},
                {"title": "Contact Us", "order": 40, "url": "#"},
            ],
        },
        {
            "title": "Blog",
            "order": 40,
            "url": "#",
            "items": [],
        },
        {
            "title": "Contact Us",
            "order": 50,
            "url": "#",
            "items": [],
        },
    ]

    for p in pages:
        slug = slugify(p["title"])
        page, _ = MainPage.objects.get_or_create(
            slug=slug,
            defaults={
                "title": p["title"],
                "url": p["url"],
                "order": p["order"],
                "is_active": True,
            },
        )
        for it in p["items"]:
            DropdownItem.objects.get_or_create(
                main_page=page,
                title=it["title"],
                defaults={
                    "url": it["url"],
                    "order": it["order"],
                    "is_active": True,
                },
            )


def unseed_navigation(apps, schema_editor):
    MainPage = apps.get_model("core", "MainPage")
    DropdownItem = apps.get_model("core", "DropdownItem")
    titles = [
        "Prospective Customers",
        "Existing Customers",
        "About Us",
        "Blog",
        "Contact Us",
    ]
    for t in titles:
        try:
            page = MainPage.objects.get(title=t)
            DropdownItem.objects.filter(main_page=page).delete()
            page.delete()
        except MainPage.DoesNotExist:
            continue


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_mainpage_slug"),
    ]

    operations = [
        migrations.RunPython(seed_navigation, unseed_navigation),
    ]

