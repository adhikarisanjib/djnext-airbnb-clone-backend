from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import AccessToken

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from useraccount.models import CustomUser
from property.models import Property, Reservation
from property.serializers import PropertyListSerializer, PropertyDetailSerializer, ReservationListSerializer
from property.forms import PropertyForm


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_list(request):
    
    try:
        token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
        token = AccessToken(token)
        user_id = token.payload.get("user_id")
        user = CustomUser.objects.get(id=user_id)
    except Exception as e:
        user = None
    
    favourites = []
    properties = Property.objects.all()
    
    landlord_id = request.GET.get("landlord_id", "")
    if landlord_id:
        properties = properties.filter(landloard_id=landlord_id)

    is_favourites = request.GET.get("is_favourites", "")
    if is_favourites:
        properties = properties.filter(favourite__in=[user])

    country = request.GET.get("country", "")
    category = request.GET.get("category", "")
    checkin_date = request.GET.get("checkIn", "")
    checkout_date = request.GET.get("checkOut", "")
    bedrooms = request.GET.get("numBedrooms", "")
    bathrooms = request.GET.get("numBathrooms", "")
    guests = request.GET.get("numGuests", "")

    if checkin_date and checkout_date:
        exact_matches = Reservation.objects.filter(start_date=checkin_date) | Reservation.objects.filter(end_date=checkout_date)
        overlap_matches = Reservation.objects.filter(start_date__lte=checkout_date, end_date__gte=checkin_date)
        all_matches = []

        for reservation in exact_matches | overlap_matches:
            all_matches.append(reservation.property.id)

        properties = properties.exclude(id__in=all_matches)

    if guests:
        properties = properties.filter(max_guests__gte=guests)

    if bedrooms:
        properties = properties.filter(bedrooms__gte=bedrooms)

    if bathrooms:
        properties = properties.filter(bathrooms__gte=bathrooms)

    if country:
        properties = properties.filter(country=country)

    if category and category != "undefined":
        properties = properties.filter(category=category)
        
    if user:
        for property in properties:
            if user in property.favourite.all():
                favourites.append(property.id)

    serializer = PropertyListSerializer(properties, many=True)
    return JsonResponse({"data": serializer.data, 'favourites': favourites}, safe=False)


@api_view(['POST', 'FILES'])
def create_property(request):
    form = PropertyForm(request.POST, request.FILES)
    if form.is_valid():
        property = form.save(commit=False)
        property.landloard = request.user
        property.save()
        return JsonResponse({"success": "Property created successfully"})
    return JsonResponse({"errors": form.errors.as_json()}, status=400)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_detail(request, id):
    try:
        property = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return JsonResponse({"error": "Property not found"}, status=404)
    serializer = PropertyDetailSerializer(property)
    return JsonResponse({"data": serializer.data})


@api_view(["POST"])
def book_property(request, id):
    try:
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")
        number_of_guests = request.data.get("number_of_guests")
        number_of_nights = request.data.get("number_of_nights")
        total_price = request.data.get("total_price")

        property = Property.objects.get(id=id)

        reservation = Reservation(
            property=property,
            start_date=start_date,
            end_date=end_date,
            number_of_guests=number_of_guests,
            number_of_nights=number_of_nights,
            total_price=total_price,
            created_by=request.user
        )

        reservation.save()
        return JsonResponse({"success": "Property booked successfully"}, status=201)

    except Exception as e:
        print("Errors", e)
        return JsonResponse({"errors": str(e)}, status=400)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_reservations(request, id):
    try:
        property = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return JsonResponse({"errors": "Property not found"}, status=404)
    
    reservations = property.reservations.all()
    serializer = ReservationListSerializer(reservations, many=True)
    
    return JsonResponse({"data": serializer.data}, safe=False)


@api_view(['POST'])
def toggle_favourite(request, id):
    try:
        property = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return JsonResponse({"errors": "Property not found"}, status=404)
    
    if request.user in property.favourite.all():
        property.favourite.remove(request.user)
        return JsonResponse({"is_favorite": False, "success": "Property removed from favourites"})
    else:
        property.favourite.add(request.user)
        return JsonResponse({"is_favorite": True, "success": "Property added to favourites"})

