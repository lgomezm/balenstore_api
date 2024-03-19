from django.db import models


class QuotationVisitStatus(models.TextChoices):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"


class QuotationVisit(models.Model):
    scheduled_at = models.DateTimeField(blank=False)
    name = models.CharField(max_length=30, blank=False)
    address_1 = models.CharField(max_length=30, blank=False)
    address_2 = models.CharField(max_length=30, blank=False)
    city = models.CharField(max_length=30, blank=False)
    state = models.CharField(max_length=30, blank=False)
    zip = models.CharField(max_length=30, blank=False)
    status = models.CharField(
        max_length=30, blank=False, choices=QuotationVisitStatus.choices
    )
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)


class Item(models.Model):
    name = models.CharField(max_length=30, blank=False)
    year = models.IntegerField()
    manufacturer = models.CharField(max_length=30, blank=False)
    country = models.CharField(max_length=30, blank=False)
    description = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    quotation_visit = models.ForeignKey(QuotationVisit, on_delete=models.CASCADE)
