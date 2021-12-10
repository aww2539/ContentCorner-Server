from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from CreatorCornerapi.models import Creator, Group

class GroupView(ViewSet):
    def create(self, request):
        creator = Creator.objects.get(user=request.auth.user)

        try:
            group = Group.objects.create(
                title=request.data['title'],
                description=request.data['description'],
                timestamp=request.data['timestamp'],
                creator=creator
            )
            serializer = GroupSerializer(group, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        group = Group.objects.get(pk=pk)
        serializer = GroupSerializer(group, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST', 'DELETE'], detail=True)
    def join(self, request, pk=None):
        # url: /groups/pk/join

        creator = Creator.objects.get(user=request.auth.user)
        group = Group.objects.get(pk=pk)

        if request.method == 'POST':
            group.members.add(creator)
            return Response({}, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            group.members.remove(creator)
            return Response({}, status=status.HTTP_204_NO_CONTENT)

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
        fields = ['id', 'title', 'description', 'timestamp', 'creator', 'members']
        depth = 2