from django import forms

from property.models import Property


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            "title",
            "description",
            "price_per_night",
            "bedrooms",
            "bathrooms",
            "max_guests",
            "country",
            "country_code",
            "category",
            "image",
        ]
