from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from GameCollectionAPI.models import Rating, Game

User = get_user_model()

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'title', 'cover_art', 'genre', 'developer', 'release_date', 'platform_id', 'length')

class RatingSerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)
    game_id = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all(), source='game', write_only=True)

    class Meta:
        model = Rating
        fields = ('id', 'user', 'game', 'game_id', 'score')

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        game_id = request.data.get('game_id')
        score = request.data.get('score')

        # Validate the input for game_id and score
        if not game_id or score is None:
            return Response({"error": "Missing game_id or score"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            score = int(score)  # Ensure the score is an integer
        except ValueError:
            return Response({"error": "Invalid score format"}, status=status.HTTP_400_BAD_REQUEST)

        rating, created = Rating.objects.update_or_create(
            user=user,
            game_id=game_id,
            defaults={'score': score}
        )

        serializer = self.get_serializer(rating)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)