from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from GameCollectionAPI.models import Game, Collection
from rest_framework import serializers
from GameCollectionAPI.models import Game, Collection

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)
    class Meta:
        model = Collection
        fields = ('id', 'user', 'game')

User = get_user_model()

class CollectionViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for managing game collections.
    """

    def create(self, request):
        """
        POST a game to a user's collection.
        """
        user = request.user
        game_id = request.data.get('game_id')

        if not game_id:
            return Response({'error': 'Game ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            game = Game.objects.get(pk=game_id)
            collection, created = Collection.objects.get_or_create(user=user, game=game)
            if created:
                return Response({'message': 'Game added to collection'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Game already in collection'}, status=status.HTTP_200_OK)
        except Game.DoesNotExist:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        DELETE a game from a user's collection.
        """
        user = request.user
        try:
            collection = Collection.objects.get(pk=pk, user=user)
            collection.delete()
            return Response({'message': 'Game removed from collection'}, status=status.HTTP_204_NO_CONTENT)
        except Collection.DoesNotExist:
            return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """
        GET all games in the user's collection.
        """
        user = request.user
        collections = Collection.objects.filter(user=user)
        serializer = CollectionSerializer(collections, many=True, context={'request': request})
        return Response(serializer.data)
    

class AllCollectionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Collection.objects.select_related('user', 'game').all()
    serializer_class = CollectionSerializer

    def list(self, request, *args, **kwargs):
        """
        Optionally restricts the returned collections to a given user,
        by filtering against a 'username' query parameter in the URL.
        """
        queryset = self.queryset
        username = request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(user__username=username)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)