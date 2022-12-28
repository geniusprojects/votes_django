from rest_framework import serializers

from .models import Gallery

from team.serializers import UserSerializer


class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Gallery
        fields = (
            'uid',
            'poll',
            'vote',
            'title',
            'path',
            'main',
        )