from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import viewsets, filters, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from team.models import Team

from .models import Gallery, Account, Poll
from .serializers import *


class GalleryViewSet(viewsets.ModelViewSet):
    serializer_class = GallerySerializer
    queryset = Gallery.objects.all()

    def perform_create(self, serializer):
        poll = Poll.objects.filter(uid=self.request.data['poll']).first()

        serializer.save(poll=poll)

    def get_queryset(self):
        return self.queryset