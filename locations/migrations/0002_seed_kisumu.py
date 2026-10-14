from django.db import migrations


def seed_kisumu(apps, schema_editor):
    County = apps.get_model("locations", "County")
    Town = apps.get_model("locations", "Town")
    Area = apps.get_model("locations", "Area")

    county, _ = County.objects.get_or_create(
        name="Kisumu County", defaults={"slug": "kisumu-county"}
    )
    town, _ = Town.objects.get_or_create(
        county=county, name="Kisumu",
        defaults={"slug": "kisumu-kisumu-county"},
    )
    for area_name in ["CBD", "Kondele", "Milimani", "Mamboleo", "Nyalenda", "Tom Mboya"]:
        Area.objects.get_or_create(
            town=town, name=area_name,
            defaults={"slug": f"{area_name.lower().replace(' ', '-')}-kisumu"},
        )


def unseed_kisumu(apps, schema_editor):
    County = apps.get_model("locations", "County")
    County.objects.filter(slug="kisumu-county").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_kisumu, unseed_kisumu),
    ]
