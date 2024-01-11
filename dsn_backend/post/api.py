from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer

from .forms import PostForm
from .models import Post, Like, Comment
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer

@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids)).order_by('-created_at')
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

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data
    }, safe=False)

@api_view(['POST'])
def post_create(request):
    form = PostForm(request.data)

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        user = request.user
        user.posts_count += 1
        user.save()

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add somehting here later!...'})
    
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
        return JsonResponse({'message': 'liked'})
    
@api_view(['POST'])
def post_create_comment(request, id):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)

    post = Post.objects.get(pk=id)
    post.comments.add(comment)
    post.comments_count += 1
    post.save()

    return JsonResponse({
        'comment': CommentSerializer(comment).data,
    })