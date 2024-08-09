import uuid

from django.db import models
from django.contrib.sites.models import Site

from useraccount.models import CustomUser


class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    max_guests = models.PositiveIntegerField()
    country = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    category = models.CharField(max_length=255)
    image = models.ImageField(upload_to='property_images')
    landloard = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    favourite = models.ManyToManyField(CustomUser, related_name="favourites", blank=True)

    def __str__(self):
        return self.title
    
    @property
    def image_url(self):
        if self.image:
            return f"{self.current_site.domain}{self.image.url}"
        else:
            return ""
    
    @property
    def current_site(self):
        return Site.objects.get_current()
    
    class Meta:
        verbose_name_plural = 'Properties'


class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, related_name="reservations", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_guests = models.PositiveIntegerField()
    number_of_nights = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(CustomUser, related_name="reservations", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property.title} - {self.start_date} to {self.end_date}"
