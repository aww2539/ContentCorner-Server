from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from CreatorCornerapi.models import Creator, Group, Category, Post, Comment


class CommentView(ViewSet):
    def create(self, request):
        creator = Creator.objects.get(request.auth.user)
        post = Post.objects.get(pk=request.data['postId'])

        try:
            comment = Comment.objects.create(
                creator=creator,
                post=post,
                body=request.data['body'],
                timestamp=request.data['timestamp']
            )
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Comment.DoesNotExist as ex:
            return Response({'message', 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CreatorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Creator
        fields = ['user']

class GroupSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer()
    class Meta:
        model = Group
        fields = ['id', 'creator']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'label']

class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    group = GroupSerializer()
    creator = CreatorSerializer()

    class Meta:
        model = Post
        fields = ['id', 'creator', 'group', 'category', 'title', 'body']

class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    creator = CreatorSerializer()

    class Meta:
        model = Post
        fields = ['id', 'post', 'creator', 'body', 'timestamp']