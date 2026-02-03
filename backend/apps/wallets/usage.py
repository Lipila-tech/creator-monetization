from django.db import models
from django.utils import timezone


class CreatorUsage(models.Model):
    school = models.OneToOneField(
        "apps.creators.CreatorProfile",
        on_delete=models.CASCADE, related_name="usage"
    )

    # Core counters
    students_count = models.PositiveIntegerField(default=0)
    teachers_count = models.PositiveIntegerField(default=0)

    # Monthly tracked usage
    fee_payments_this_month = models.PositiveIntegerField(default=0)
    receipt_uploads_this_month = models.PositiveIntegerField(default=0)

    # Reset tracking
    last_reset = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Usage for {self.school.name}"
