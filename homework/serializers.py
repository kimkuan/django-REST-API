from .models import Essay, Album, Files
from rest_framework import serializers

class EssaySerializer(serializers.ModelSerializer):
    
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Essay
        fields = ['pk', 'title', 'body', 'author_name']


class AlbumSerializer(serializers.ModelSerializer):
    
    author_name = serializers.ReadOnlyField(source='author.username')
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Album
        fields = ['pk', 'image', 'description', 'author_name']
        

class FileSerializer(serializers.ModelSerializer):
    
    author = serializers.ReadOnlyField(source='author.username')
    myfile = serializers.FileField(use_url=True)

    class Meta:
        model = Files
        fields = ['pk', 'myfile', 'description', 'author']
        # fileserializer에서는 files 모델과 이름 같게 해라