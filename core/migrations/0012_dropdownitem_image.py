from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_dropdownitem_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="dropdownitem",
            name="image",
            field=models.ImageField(
                upload_to="dropdown/cards/", blank=True, null=True
            ),
        ),
    ]

