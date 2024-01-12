from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from notification.utils import create_notification

from .models import User, FriendshipRequest
from .serializers import UserSerializer, FriendshipRequestSerializer
from .forms import SignupForm, ProfileForm

@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar': request.user.get_avatar(),
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message= 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        user = form.save()
        user.is_active = False
        user.save()

        url = f'http://127.0.0.1:8000/api/activate-account/?email={user.email}&id={user.id}'
        send_mail(
            "Activate your account",
            f"Click the following link to activate your account: {url}",
            "noreply@dsn.com",
            [user.email],
            fail_silently=False,
        )
    else:
        message = form.errors.as_json()

    return JsonResponse({'message': message}, safe=False)


@api_view(['POST'])
def edit_profile(request):
    user = request.user

    form = ProfileForm(request.POST, request.FILES, instance=user)
    if form.is_valid():
        form.save()
        serializer = UserSerializer(user)
        return JsonResponse({
            'message': 'updated',
            'user': serializer.data,
        })
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)


@api_view(['POST'])
def edit_password(request):
    user = request.user
    form = PasswordChangeForm(user=user, data=request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'updated'})
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)


@api_view(['GET'])
def friends(request, id):
    user = User.objects.get(pk=id)
    requests = []

    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for=request.user, status='pending')

    friends = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': FriendshipRequestSerializer(requests, many=True).data,
    }, safe=False)


@api_view(['POST'])
def send_friendship_request(request, id):
    user = User.objects.get(pk=id)

    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if not check1 or not check2:
        friendship_request = FriendshipRequest.objects.create(created_for=user, created_by=request.user)
        create_notification(request, 'friend_request', friend_request_id=friendship_request.id)
        return JsonResponse({'message': 'friendship request created'})
    else:
        return JsonResponse({'message': 'request already sent'})


@api_view(['POST'])
def handle_friendship_request(request, id, status):
    user = User.objects.get(pk=id)
    friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    friendship_request.status = status
    friendship_request.save()

    if status == 'rejected':
        create_notification(request, 'friend_reject', friend_request_id=friendship_request.id)
        return JsonResponse({'message': 'friendship request rejected'})

    user.friends.add(request.user)
    user.friends_count = user.friends_count + 1
    user.save()

    request_user = request.user
    request_user.friends.add(user)
    request_user.friends_count = request_user.friends_count + 1
    request_user.save()

    create_notification(request, 'friend_accept', friend_request_id=friendship_request.id)

    return JsonResponse({'message': 'friendship request accepted'})