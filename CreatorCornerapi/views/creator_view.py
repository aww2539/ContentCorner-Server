from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from CreatorCornerapi.models import Creator

class CreatorView(ViewSet):
    def list(self, request):
        creators = Creator.objects.all()

        creators_serializer = CreatorSerializer(creators, many=True, context={'request': request})
        return Response(creators_serializer.data)

    def retrieve(self, request, pk):
        try:
            creator = Creator.objects.get(pk=pk)

            serializer = CreatorSerializer(creator, context={'request': request})
            return Response(serializer.data)
        except Creator.DoesNotExist as ex:
            return Response({'message': 'Creator does not exist'}, status=status.HTTP_404_NOT_FOUND)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CreatorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Creator
        fields = ['user']
        depth = 1
