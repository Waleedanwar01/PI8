from django.db import migrations

def seed_atlas_partner(apps, schema_editor):
    PaymentPartner = apps.get_model("core", "PaymentPartner")
    
    # Create Atlas Partner
    PaymentPartner.objects.get_or_create(
        name="Atlas",
        defaults={
            "description": "Quickly pay your Atlas bill online",
            "payment_url": "https://www.atlas-fin.com/Customers/OnlinePayments.aspx",
            "order": 1,
            "is_active": True
        }
    )

def reverse_seed(apps, schema_editor):
    # We don't delete on reverse to avoid data loss if user edited it
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_paymentpartner'),
    ]

    operations = [
        migrations.RunPython(seed_atlas_partner, reverse_seed),
    ]
