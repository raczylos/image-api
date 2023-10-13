import imghdr
import os
from datetime import datetime, timedelta
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.signing import TimestampSigner
from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from images.models import Image
from images.serializer import ImageSerializer
from users.models import User
from rest_framework.exceptions import PermissionDenied, ValidationError


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Image.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            raise PermissionDenied("You must be logged in to upload images!")
        plan = user.role

        original_image = request.data.get('original_image')
        valid_formats = ['jpeg', 'png']
        img_format = imghdr.what(original_image)
        if not img_format or img_format not in valid_formats:
            raise ValidationError("Invalid image format! Please upload a JPEG or PNG image!")

        serializer = ImageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user_image = serializer.save(user=user)

            if plan == User.Role.BASIC:
                user_image.thumbnail_200 = generate_thumbnail(user_image.original_image, 200, img_format)
                user_image.original_image.delete()
            elif plan == User.Role.PREMIUM:
                user_image.thumbnail_200 = generate_thumbnail(user_image.original_image, 200, img_format)
                user_image.thumbnail_400 = generate_thumbnail(user_image.original_image, 400, img_format)
            elif plan == User.Role.ENTERPRISE:
                user_image.thumbnail_200 = generate_thumbnail(user_image.original_image, 200, img_format)
                user_image.thumbnail_400 = generate_thumbnail(user_image.original_image, 400, img_format)

            user_image.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def generate_thumbnail(image, height, img_format):
    from PIL import Image

    image_name = image.name
    image = Image.open(image)
    image_base_name = os.path.splitext(os.path.basename(image_name))[0]

    image.thumbnail((image.width, height))
    thumbnail_io = BytesIO()
    image.save(thumbnail_io, img_format)

    thumbnail_name = f"files/thumbnails/thumbnail_{height}_{image_base_name}.{img_format}"

    default_storage.save(thumbnail_name, ContentFile(thumbnail_io.getvalue()))

    return thumbnail_name


