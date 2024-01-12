from .models import Notification

from post.models import Post
from account.models import FriendshipRequest

def create_notification(request, type, post_id=None, friend_request_id=None):
    '''
    Create a notification based on the given parameters.

    Args:
        request (HttpRequest): The HTTP request object.
        type (str): The type of notification. Possible values are 'like', 'comment', 'friend_request', 'friend_accept', 'friend_reject'.
        post_id (str uuid, optional): The ID of the post related to the notification. Defaults to None.
        friend_request_id (str uuid, optional): The ID of the friend request related to the notification. Defaults to None.

    Returns:
        Notification: The created notification object.
    '''
    sent_to = None

    if type == 'like':
        sent_to = Post.objects.get(pk=post_id).created_by
        body = f'{request.user.name} liked one of your posts!'
    elif type == 'comment':
        sent_to = Post.objects.get(pk=post_id).created_by
        body = f'{request.user.name} commented on one of your posts!'
    elif type == 'friend_request':
        sent_to = FriendshipRequest.objects.get(pk=friend_request_id).created_for
        body = f'{request.user.name} sent you a friend request!'
    elif type == 'friend_accept':
        sent_to = FriendshipRequest.objects.get(pk=friend_request_id).created_for
        body = f'{request.user.name} accepted your friend request!'
    elif type == 'friend_reject':
        sent_to = FriendshipRequest.objects.get(pk=friend_request_id).created_for
        body = f'{request.user.name} rejected your friend request!'

    notification = Notification.objects.create(
        body=body,
        type=type,
        post=Post.objects.get(pk=post_id) if post_id else None,
        created_by=request.user,
        sent_to=sent_to
    )
    return notification