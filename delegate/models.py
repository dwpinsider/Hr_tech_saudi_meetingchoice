from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Delegate(models.Model):
    Destination = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100) #Type
    country = models.CharField(max_length=100)
    branding = models.CharField(max_length=100)
    solutions = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = "delegates"


class DelegateMeetingRegister(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255)
    day_of_participation = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    delegates = models.ManyToManyField(Delegate)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.company_name})"

