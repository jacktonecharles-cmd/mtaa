from django.db import migrations

CATEGORIES = [
    ("Salons", "fa-solid fa-scissors"),
    ("Barbers", "fa-solid fa-scissors"),
    ("Restaurants", "fa-solid fa-utensils"),
    ("Hotels", "fa-solid fa-bed"),
    ("Clothing Shops", "fa-solid fa-shirt"),
    ("Shoe Shops", "fa-solid fa-shoe-prints"),
    ("Electronics Shops", "fa-solid fa-tv"),
    ("Phone Shops", "fa-solid fa-mobile-screen"),
    ("Computer Shops", "fa-solid fa-computer"),
    ("Photographers", "fa-solid fa-camera"),
    ("Mechanics", "fa-solid fa-wrench"),
    ("Car Washes", "fa-solid fa-car"),
    ("Tailors", "fa-solid fa-scroll"),
    ("Beauty Businesses", "fa-solid fa-spa"),
    ("Wigs & Hair", "fa-solid fa-wand-magic-sparkles"),
    ("Makeup Artists", "fa-solid fa-palette"),
    ("Event Planners", "fa-solid fa-calendar-check"),
    ("DJs", "fa-solid fa-music"),
    ("Caterers", "fa-solid fa-utensils"),
    ("Plumbers", "fa-solid fa-faucet"),
    ("Electricians", "fa-solid fa-bolt"),
    ("Painters", "fa-solid fa-paint-roller"),
    ("Construction Services", "fa-solid fa-trowel-bricks"),
    ("Tutors", "fa-solid fa-graduation-cap"),
    ("Web Developers", "fa-solid fa-code"),
    ("Graphic Designers", "fa-solid fa-pen-nib"),
    ("Printing Services", "fa-solid fa-print"),
    ("Cyber Cafes", "fa-solid fa-desktop"),
    ("Gyms", "fa-solid fa-dumbbell"),
    ("Furniture Shops", "fa-solid fa-couch"),
    ("Supermarkets", "fa-solid fa-cart-shopping"),
    ("Hardware Stores", "fa-solid fa-hammer"),
    ("Pharmacies", "fa-solid fa-pills"),
    ("Auto Parts", "fa-solid fa-car-side"),
    ("Transport Services", "fa-solid fa-bus"),
    ("Other", "fa-solid fa-ellipsis"),
]


def seed_categories(apps, schema_editor):
    Category = apps.get_model("categories", "Category")
    from django.utils.text import slugify
    for order, (name, icon) in enumerate(CATEGORIES):
        Category.objects.get_or_create(
            name=name,
            defaults={"slug": slugify(name), "icon": icon, "order": order},
        )


def unseed_categories(apps, schema_editor):
    Category = apps.get_model("categories", "Category")
    Category.objects.filter(name__in=[c[0] for c in CATEGORIES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_categories, unseed_categories),
    ]
