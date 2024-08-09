from django.urls import path

from property.api import property_list, create_property, property_detail, book_property, property_reservations, toggle_favourite

urlpatterns = [
    path('', property_list, name='property_list'),
    path('create/', create_property, name='create_property'),
    path('<uuid:id>/', property_detail, name='property_detail'),
    path('<uuid:id>/book/', book_property, name='book_property'),
    path('<uuid:id>/reservations/', property_reservations, name='property_reservations'),
    path('<uuid:id>/toggle_favourite/', toggle_favourite, name='toggle_favourite'),
]
