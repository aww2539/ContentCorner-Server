from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from CreatorCornerapi.models import Creator, Group, Category, Post


class PostView(ViewSet):
    def create(self, request):
        creator = Creator.objects.get(request.auth.user)
        group = Group.objects.get(pk=request.data['groupId'])
        category = Category.objects.get(pk=request.data['categoryId'])

        try:
            post = Post.objects.create(
                creator=creator,
                group=group,
                category=category,
                title=request.data['title'],
                body=request.data['body'],
                timestamp=request.data['timestamp']
            )
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        category = self.request.query_params.get("category",None)
        creator = self.request.query_params.get("creator",None)
        group = self.request.query_params.get("group",None)
        posts = Post.objects.all()

        if category is not None:
            posts = posts.filter(category__id=category)

        if creator is not None:
            posts = posts.filter(creator__id=creator)

        if group is not None:
            posts = posts.filter(group__id=group)

        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Post.DoesNotExist as ex:
            return Response({'message', 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CreatorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Creator
        fields = ['user']

class GroupSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer()
    class Meta:
        model = Group
        fields = ['id', 'title', 'description', 'timestamp', 'creator']


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
        fields = ['id', 'creator', 'group', 'category', 'title', 'body', 'timestamp']
