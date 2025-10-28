from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from delegate.models import Delegate ,DelegateMeetingRegister

class VendorPlanner(models.Model):
    company_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    company_type = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    asia_pacific = models.CharField(max_length=500, null=True, blank=True)
    middle_east_africa = models.CharField(max_length=500, null=True, blank=True)
    europe = models.CharField(max_length=500, null=True, blank=True)
    russia_eastern_europe_cis = models.CharField(max_length=500, null=True, blank=True)
    north_america = models.CharField(max_length=500, null=True, blank=True)
    canada = models.CharField(max_length=500, null=True, blank=True)
    south_central_america = models.CharField(max_length=500, null=True, blank=True)
    africa = models.CharField(max_length=500, null=True, blank=True)
    caribbean = models.CharField(max_length=500, null=True, blank=True)
    budget_for_events = models.CharField(max_length=255, null=True, blank=True)
    weddings_per_year = models.CharField(max_length=255, null=True, blank=True)
    top_6_corporate_clients = models.CharField(max_length=500, null=True, blank=True)

    is_active = models.BooleanField(default=True, verbose_name=_('Active'))

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = "Vendors"


class VendorMeetingRegister(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company_name =models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    vendors = models.ManyToManyField(VendorPlanner)
    delegates = models.ManyToManyField(DelegateMeetingRegister, related_name='delegate_meeting_registers')
    Delegate = models.ManyToManyField(Delegate, related_name='delegate')


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.company_name})"

    @property
    def selected_delegates(self):
        return [delegate.company_name for delegate in self.delegates.all()]

