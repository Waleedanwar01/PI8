from django.db import migrations, models
from django.utils.text import slugify


def populate_dropdownitem_slug(apps, schema_editor):
    DropdownItem = apps.get_model("core", "DropdownItem")
    for item in DropdownItem.objects.all():
        if item.slug:
            continue
        base_slug = slugify(item.title) or "item"
        slug = base_slug
        idx = 1
        qs = DropdownItem.objects
        while qs.filter(slug=slug).exclude(pk=item.pk).exists():
            idx += 1
            slug = f"{base_slug}-{idx}"
        item.slug = slug
        item.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_page_layout_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="dropdownitem",
            name="slug",
            field=models.SlugField(max_length=150, blank=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="dropdownitem",
            name="url",
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.RunPython(populate_dropdownitem_slug, migrations.RunPython.noop),
    ]
