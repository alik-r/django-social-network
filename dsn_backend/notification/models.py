import uuid 

from django.db import models

from account.models import User
from post.models import Post

class Notification(models.Model):
    TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('friend_request', 'Friend Request'),
        ('friend_accept', 'Friend Accept'),
        ('friend_reject', 'Friend Reject'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_notifications')
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body