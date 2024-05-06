from django.db import models, transaction
from django import forms
import datetime
from django.views.decorators.csrf import csrf_exempt 
from rest_framework import viewsets, serializers, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.utils.timezone import make_aware
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from GameCollectionAPI.models import Game, Platform

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'name']


    def to_internal_value(self, data):
        if isinstance(data, int):  # Handling integer ID inputs directly
            return {'id': data}
        elif isinstance(data, dict):  # Handling dictionary inputs as usual
            return super(PlatformSerializer, self).to_internal_value(data)
        else:
            raise serializers.ValidationError("Expected either an integer ID or a dictionary.")

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'title', 'cover_art', 'genre', 'developer', 'release_date', 'creator', 'platforms')
        extra_kwargs = {'creator': {'read_only': True}}

    def create(self, validated_data):
        print("Validated data:", validated_data)
        platforms_data = validated_data.pop('platforms', [])
        print("Platforms data:", platforms_data)
        game = Game.objects.create(**validated_data)
        for platform in platforms_data:
            game.platforms.add(platform)
        game.save()
        return game

    def update(self, instance, validated_data):
        platforms_data = validated_data.pop('platforms', None)
        if platforms_data is not None:
            instance.platforms.clear()
            for platform in platforms_data:
                instance.platforms.add(platform)

    # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class GamePagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100

class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creators of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the creator of the game.
        return obj.creator == request.user

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'genre', 'developer']  # Allows searching by game title, genre, or developer
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]

    def perform_create(self, serializer):
        print("Validated data:", serializer.validated_data)
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save(creator=self.request.user) 


class PlatformViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        print("Accessing PlatformViewSet")
        return super().list(request, *args, **kwargs)
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]

            # Check if many is not already set and data is a list
            if isinstance(data, list):
                kwargs["many"] = True

        return super(PlatformViewSet, self).get_serializer(*args, **kwargs)