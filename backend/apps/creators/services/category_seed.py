from django.db import transaction
from apps.creators.models import CreatorCategory


ZAMBIA_CATEGORIES = [
    # Featured (top)
    {"name": "Music & DJs", "slug": "music-djs", "icon": "music", "is_featured": True, "sort_order": 10},
    {"name": "Comedy", "slug": "comedy", "icon": "laugh", "is_featured": True, "sort_order": 20},
    {"name": "Faith & Spiritual", "slug": "faith-spiritual", "icon": "church", "is_featured": True, "sort_order": 30},
    {"name": "Education & Tutoring", "slug": "education-tutoring", "icon": "graduation-cap", "is_featured": True, "sort_order": 40},
    {"name": "Fitness & Wellness", "slug": "fitness-wellness", "icon": "dumbbell", "is_featured": True, "sort_order": 50},
    {"name": "Beauty (Makeup/Hair)", "slug": "beauty", "icon": "sparkles", "is_featured": True, "sort_order": 60},
    {"name": "Fashion & Style", "slug": "fashion-style", "icon": "shirt", "is_featured": True, "sort_order": 70},
    {"name": "Food & Cooking", "slug": "food-cooking", "icon": "utensils", "is_featured": True, "sort_order": 80},
    {"name": "Business & Entrepreneurship", "slug": "business-entrepreneurship", "icon": "briefcase", "is_featured": True, "sort_order": 90},
    {"name": "Tech (Developers/Tech Education)", "slug": "tech", "icon": "laptop", "is_featured": True, "sort_order": 100},

    # Non-featured (still useful for filtering)
    {"name": "Photography", "slug": "photography", "icon": "camera", "is_featured": False, "sort_order": 200},
    {"name": "Videography", "slug": "videography", "icon": "video", "is_featured": False, "sort_order": 210},
    {"name": "Content Creator", "slug": "content-creator", "icon": "clapperboard", "is_featured": False, "sort_order": 220},
    {"name": "Podcasts & Radio", "slug": "podcasts-radio", "icon": "mic", "is_featured": False, "sort_order": 230},
    {"name": "Art & Design", "slug": "art-design", "icon": "palette", "is_featured": False, "sort_order": 240},
    {"name": "Dance", "slug": "dance", "icon": "music-2", "is_featured": False, "sort_order": 250},
    {"name": "Lifestyle", "slug": "lifestyle", "icon": "sun", "is_featured": False, "sort_order": 260},
    {"name": "Travel", "slug": "travel", "icon": "map", "is_featured": False, "sort_order": 270},
]


@transaction.atomic
def seed_zambia_creator_categories(country_code: str = "ZM") -> dict:
    created = 0
    updated = 0

    for item in ZAMBIA_CATEGORIES:
        defaults = {
            "name": item["name"],
            "icon": item.get("icon", ""),
            "is_featured": item.get("is_featured", False),
            "country_code": country_code,
            "is_active": True,
            "sort_order": item.get("sort_order", 100),
        }
        obj, was_created = CreatorCategory.objects.update_or_create(
            slug=item["slug"],
            defaults=defaults,
        )
        if was_created:
            created += 1
        else:
            updated += 1

    return {"created": created, "updated": updated}
