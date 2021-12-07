from rest_framework import status
from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from CreatorCornerapi.models import Category

class CategoryView(ViewSet):
    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Category.DoesNotExist as ex:
            return Response({'message', 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

class CategorySerializer(serializers.ModelSerializer):
    '''JSON serializer for categories'''
    class Meta:
        model = Category
        fields = ['id', 'label']
