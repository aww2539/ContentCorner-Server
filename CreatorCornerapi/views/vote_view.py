from rest_framework import status
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from CreatorCornerapi.models import Vote, Creator, Post, Category, Group

class VoteView(ViewSet):
    def list(self, request):
        post = self.request.query_params.get("post",None)
        creator = self.request.query_params.get("creator",None)

        votes = Vote.objects.all()

        if post is not None:
            votes = votes.filter(post__id=post)

        if creator is not None:
            votes = votes.filter(creator__id=creator)

        serializer = VoteSerializer(votes, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            vote = Vote.objects.get(pk=pk)
            serializer = VoteSerializer(vote, context={'request': request})
            return Response(serializer.data)
        except Vote.DoesNotExist as ex:
            return Response({'message', 'Vote not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        creator = Creator.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=request.data['postId'])

        try:
            vote = Vote.objects.create(
                creator = creator,
                post = post,
                upvote = request.data['upvote'],
                downvote = request.data['downvote'],
            )
            serializer = VoteSerializer(vote, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):

        creator = Creator.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=request.data['postId'])

        vote = Vote.objects.get(pk=pk)
        vote.creator = creator
        vote.post = post
        vote.upvote = request.data['upvote']
        vote.downvote = request.data['downvote']
        vote.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CreatorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Creator
        fields = ['user']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'label']

class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    creator = CreatorSerializer()

    class Meta:
        model = Post
        fields = ['id', 'creator', 'group', 'category']

class VoteSerializer(serializers.ModelSerializer):
    '''JSON serializer for votes'''
    # creator = CreatorSerializer()
    # post = PostSerializer()

    class Meta:
        model = Vote
        fields = ['id', 'creator', 'post', 'upvote', 'downvote']
        depth = 1
