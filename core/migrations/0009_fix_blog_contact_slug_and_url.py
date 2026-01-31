from django.db import migrations
from django.utils.text import slugify


def fix_blog_contact(apps, schema_editor):
    MainPage = apps.get_model("core", "MainPage")

    titles = ["Blog", "Contact Us"]
    for title in titles:
        try:
            page = MainPage.objects.get(title=title)
        except MainPage.DoesNotExist:
            continue

        if not page.slug:
            page.slug = slugify(title)
        # Let template use get_absolute_url instead of "#"
        page.url = ""
        page.is_active = True
        page.save()


def reverse_fix_blog_contact(apps, schema_editor):
    # Do nothing on reverse; non-destructive migration
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_update_nav_structure"),
    ]

    operations = [
        migrations.RunPython(fix_blog_contact, reverse_fix_blog_contact),
    ]

