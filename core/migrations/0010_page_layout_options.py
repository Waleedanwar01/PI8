from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_fix_blog_contact_slug_and_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="mainpage",
            name="content_width",
            field=models.CharField(
                max_length=20,
                choices=[
                    ("default", "Centered (medium width)"),
                    ("wide", "Wide content"),
                    ("full", "Full width"),
                ],
                default="default",
            ),
        ),
        migrations.AddField(
            model_name="mainpage",
            name="layout_columns",
            field=models.PositiveSmallIntegerField(
                default=1,
                choices=[
                    (1, "Single column"),
                    (2, "Two columns"),
                    (3, "Three columns"),
                ],
            ),
        ),
        migrations.AddField(
            model_name="dropdownitem",
            name="content_width",
            field=models.CharField(
                max_length=20,
                choices=[
                    ("default", "Centered (medium width)"),
                    ("wide", "Wide content"),
                    ("full", "Full width"),
                ],
                default="default",
            ),
        ),
        migrations.AddField(
            model_name="dropdownitem",
            name="layout_columns",
            field=models.PositiveSmallIntegerField(
                default=1,
                choices=[
                    (1, "Single column"),
                    (2, "Two columns"),
                    (3, "Three columns"),
                ],
            ),
        ),
    ]
