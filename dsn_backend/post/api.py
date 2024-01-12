from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User, FriendshipRequest
from account.serializers import UserSerializer

from notification.utils import create_notification

from .forms import PostForm, PostAttachmentForm
from .models import Post, Like, Comment, Trend
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer

@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids)).order_by('-created_at')

    trend_id = request.GET.get('trend', None)
    if trend_id is not None:
        trend = Trend.objects.get(pk=trend_id).title
        posts = posts.filter(body__icontains=trend)

    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def post_detail(request, id):
    post = Post.objects.get(pk=id)
    return JsonResponse({
        'post': PostDetailSerializer(post).data,
    })

@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    can_send_friendship_request = True

    if request.user in user.friends.all():
        can_send_friendship_request = False

    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if check1 or check2:
        can_send_friendship_request = False

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data,
        'can_send_friendship_request': can_send_friendship_request,
    }, safe=False)

@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    attachment_form = PostAttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment is not None:
            post.attachments.add(attachment)
            post.save()

        user = request.user
        user.posts_count += 1
        user.save()

        serializer = PostSerializer(post)
        
        return JsonResponse({
            'message': 'success',
            'post': serializer.data
        }, safe=False)
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)
    
@api_view(['POST'])
def post_like(request, id):
    post = Post.objects.get(pk=id)
    user = request.user

    if post.likes.filter(created_by_id=user.id).exists():
        post.likes.filter(created_by_id=user.id).delete()
        post.likes_count -= 1
        post.save()
        return JsonResponse({'message': 'unliked'})
    else:
        like = Like.objects.create(created_by=user)
        post.likes.add(like)
        post.likes_count += 1
        post.save()

        create_notification(request, 'like', post_id=post.id)

        return JsonResponse({'message': 'liked'})
    
@api_view(['POST'])
def post_create_comment(request, id):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)

    post = Post.objects.get(pk=id)
    post.comments.add(comment)
    post.comments_count += 1
    post.save()

    create_notification(request, 'comment', post_id=post.id)

    return JsonResponse({
        'comment': CommentSerializer(comment).data,
    })

@api_view(['GET'])
def trend_list(request):
    serializer = TrendSerializer(Trend.objects.all(), many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def trend_detail(request, id):
    serializer = TrendSerializer(Trend.objects.get(pk=id))
    return JsonResponse(serializer.data, safe=False)