from rest_framework import serializers

from account.serializers import UserSerializer

from .models import Post, PostAttachment, Comment, Trend

class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ('id', 'get_image',)


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = PostAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'created_by', 'created_at_formatted', 'attachments',)


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'body', 'created_by', 'created_at_formatted',)


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    attachments = PostAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'comments','comments_count', 'created_by', 'created_at_formatted', 'attachments',)


class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ('id', 'title', 'count',)