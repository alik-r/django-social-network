from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Notification
from .serializers import NotificationSerializer

@api_view(['GET'])
def notification_list(request):
    received_notifications = request.user.received_notifications.filter(is_read=False).order_by('-created_at')
    serializer = NotificationSerializer(received_notifications, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def read_notification(request, id):
    notification = Notification.objects.filter(sent_to=request.user).get(pk=id)
    if notification is None:
        return JsonResponse({'message': 'notification not found'}, status=404)
    
    notification.is_read = True
    notification.save()

    return JsonResponse({'message': 'success'}) 