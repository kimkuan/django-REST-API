from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import serializers
from .models import Essay, Album, Files
from .serializers import EssaySerializer, AlbumSerializer, FileSerializer
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class PostViewSet(viewsets.ModelViewSet):

    queryset = Essay.objects.all()
    serializer_class = EssaySerializer

    filter_backends = [SearchFilter]
    search_fields = ('title', 'body')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):

        qs = super().get_queryset()

        if self.request.user.is_authenticated: 
            if self.request.user.username == 'admin': # admin인 경우에는 모든 글을 볼 수 있음
                qs = Essay.objects.all()
            else:
                qs = qs.filter(author=self.request.user) # 본인이 쓴 글만 볼 수 있음
              
        else:
            qs = qs.none()

        return qs


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class FileViewSet(viewsets.ModelViewSet):

    queryset = Files.objects.all()
    serializer_class = FileSerializer

    # file 업로드시 오류 해결책
    # parser_class 지정 - 다양한 미디어 파일 허용
    parser_class = (MultiPartParser, FormParser)

    # create() 오버라이드 -> post 요청
    def post(self, request, *args, **kwargs):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)
