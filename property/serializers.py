from rest_framework import serializers

from property.models import Property, Reservation

from useraccount.serializers import UserAccountDetailSerializer


class PropertyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'title', 'price_per_night', 'image_url']


class PropertyDetailSerializer(serializers.ModelSerializer):
    landloard = UserAccountDetailSerializer(read_only=True)
    
    class Meta:
        model = Property
        fields = [
            'id',
            'title',
            'description',
            'price_per_night',
            'bedrooms',
            'bathrooms',
            'max_guests',
            'country',
            'category',
            'image_url',
            'landloard',
            'created_at',
        ]
        

class ReservationListSerializer(serializers.ModelSerializer):
    property = PropertyListSerializer(read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id',
            'property',
            'start_date',
            'end_date',
            'number_of_guests',
            'number_of_nights',
            'total_price',
            'created_at',
        ]
