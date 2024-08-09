from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from useraccount.models import CustomUser
from useraccount.serializers import UserAccountDetailSerializer
from property.serializers import ReservationListSerializer


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def landlord_detail(request, id):
    print("Landlord id", id)
    try:
        user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    serializer = UserAccountDetailSerializer(user)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def reservations_list(request):
    reservations = request.user.reservations.all()
    serializer = ReservationListSerializer(reservations, many=True)
    return JsonResponse(serializer.data, safe=False)
