from rest_framework import serializers

from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'body', 'type', 'post_id', 'sent_to_id')