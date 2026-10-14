from django.db import migrations


def seed_plans(apps, schema_editor):
    Plan = apps.get_model("subscriptions", "Plan")
    Plan.objects.get_or_create(
        code="free", defaults={
            "name": "Free", "price_ksh_per_month": 0,
            "description": "Get listed at no cost.",
            "features": "Basic listing\nBusiness information\nContact information\nLimited photos",
        },
    )
    Plan.objects.get_or_create(
        code="premium", defaults={
            "name": "Premium", "price_ksh_per_month": 500,
            "description": "Stand out with a premium badge and better visibility.",
            "features": "Premium badge\nMore photos\nBetter search visibility\nBusiness statistics\nSocial links\nPriority placement",
        },
    )
    Plan.objects.get_or_create(
        code="featured", defaults={
            "name": "Featured", "price_ksh_per_month": 1500,
            "description": "Maximum visibility, right on the homepage.",
            "features": "Everything in Premium\nHomepage placement\nFeatured badge\nTop placement in category/location",
        },
    )


def unseed_plans(apps, schema_editor):
    Plan = apps.get_model("subscriptions", "Plan")
    Plan.objects.filter(code__in=["free", "premium", "featured"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_plans, unseed_plans),
    ]
