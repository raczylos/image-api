from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'user', 'original_image', 'thumbnail_200', 'thumbnail_400']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'thumbnail_200': {'read_only': True},
            'thumbnail_400': {'read_only': True},
            # 'expiring_link': {'read_only': True},
            # 'expiration_time': {'read_only': True}
        }

