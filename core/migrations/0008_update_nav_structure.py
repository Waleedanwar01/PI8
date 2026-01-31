from django.db import migrations
from django.utils.text import slugify


def update_nav(apps, schema_editor):
    MainPage = apps.get_model("core", "MainPage")
    DropdownItem = apps.get_model("core", "DropdownItem")

    pages = [
        {
            "title": "Prospective Customers",
            "order": 10,
            "url": "",
            "items": [
                {
                    "title": "Request a Quote",
                    "order": 10,
                    "url": "#",
                    "icon_svg": '<svg class="w-7 h-7 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>',
                },
                {
                    "title": "Sales & Application Support",
                    "order": 20,
                    "url": "#",
                    "icon_svg": '<svg class="w-7 h-7 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/></svg>',
                },
                {
                    "title": "Insurance Term Definitions",
                    "order": 30,
                    "url": "#",
                    "icon_svg": '<svg class="w-7 h-7 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>',
                },
                {
                    "title": "Upload a File",
                    "order": 40,
                    "url": "#",
                    "icon_svg": '<svg class="w-7 h-7 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/></svg>',
                },
            ],
        },
        {
            "title": "Existing Customers",
            "order": 20,
            "url": "",
            "items": [
                {
                    "title": "Submit a Claim",
                    "order": 10,
                    "url": "#",
                    "icon_svg": '<svg class="w-7 h-7 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16.862 4.487A2.1 2.1 0 0015.3 3.75H8.7a2.1 2.1 0 00-1.562.737L4.5 7.125V19.5A1.5 1.5 0 006 21h12a1.5 1.5 0 001.5-1.5V7.125l-2.638-3.01z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 11.25l2.25 2.25L15 9"/></svg>',
                },
                {
                    "title": "Add or Edit Vehicle or Driver List",
                    "order": 20,
                    "url": "#",
                    "icon_svg": '<svg class="w-7 h-7 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 13l2-5h14l2 5M5 18h14M7 18v-3h10v3M9 10V7h6v3"/></svg>',
                },
                {
                    "title": "Make a Payment Online",
                    "order": 30,
                    "url": "#",
                    "icon_svg": '<svg class="w-7 h-7 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7h18M5 11h14M7 15h6M5 5h14a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2z"/></svg>',
                },
                {
                    "title": "Support for Current Clients",
                    "order": 40,
                    "url": "#",
                    "icon_svg": '<svg class="w-7 h-7 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 10a6 6 0 11-12 0 6 6 0 0112 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A9 9 0 0112 15a9 9 0 016.879 2.804"/></svg>',
                },
                {
                    "title": "Upload a File",
                    "order": 50,
                    "url": "#",
                    "icon_svg": '<svg class="w-7 h-7 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/></svg>',
                },
            ],
        },
        {
            "title": "About Us",
            "order": 30,
            "url": "",
            "items": [
                {
                    "title": "Contact Information",
                    "order": 10,
                    "url": "#",
                    "icon_svg": '<svg class="w-7 h-7 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l.894 2.683a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l2.683.894A1 1 0 0121 17.72V21a2 2 0 01-2 2h-1C9.82 23 5 18.18 5 12V11a2 2 0 012-2h0"/></svg>',
                },
                {
                    "title": "About Us",
                    "order": 20,
                    "url": "#",
                    "icon_svg": '<svg class="w-7 h-7 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2a5.002 5.002 0 00-9.288-1.857M7 20H2v-2a3 3 0 015.356-1.857"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 11a4 4 0 100-8 4 4 0 000 8z"/></svg>',
                },
                {
                    "title": "Partners",
                    "order": 30,
                    "url": "#",
                    "icon_svg": '<svg class="w-7 h-7 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5 1a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
                },
                {
                    "title": "Refer a Friend",
                    "order": 40,
                    "url": "#",
                    "icon_svg": '<svg class="w-7 h-7 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h9a2 2 0 002-2v-3"/></svg>',
                },
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
        # Keep title/order/url up to date
        page.title = p["title"]
        page.url = p["url"]
        page.order = p["order"]
        page.is_active = True
        page.save()

        desired_titles = []
        for it in p["items"]:
            desired_titles.append(it["title"])
            DropdownItem.objects.update_or_create(
                main_page=page,
                title=it["title"],
                defaults={
                    "url": it["url"],
                    "order": it["order"],
                    "is_active": True,
                    "icon_svg": it.get("icon_svg", ""),
                },
            )
        # Remove any old items not in desired list for this page
        DropdownItem.objects.filter(main_page=page).exclude(title__in=desired_titles).delete()


def reverse_nav(apps, schema_editor):
    # No-op: we don't want to delete data on reverse
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_dropdownitem_content_dropdownitem_meta_description_and_more"),
    ]

    operations = [
        migrations.RunPython(update_nav, reverse_nav),
    ]

