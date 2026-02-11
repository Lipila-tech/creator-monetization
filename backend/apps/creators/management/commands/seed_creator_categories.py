# identity/management/commands/seed_creator_categories.py
from django.core.management.base import BaseCommand
from apps.creators.services.category_seed import seed_zambia_creator_categories

class Command(BaseCommand):
    help = "Seed creator categories (Zambia-first) with icons and featured flags."

    def add_arguments(self, parser):
        parser.add_argument("--country", default="ZM", help="ISO 3166-1 alpha-2 country code, default ZM")

    def handle(self, *args, **options):
        country = options["country"]
        result = seed_zambia_creator_categories(country_code=country)
        self.stdout.write(self.style.SUCCESS(
            f"Creator categories seeded for {country}. Created={result['created']} Updated={result['updated']}"
        ))

# Usage
# python manage.py seed_creator_categories --country ZM