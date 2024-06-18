from rest_framework import serializers
from .models import Article, Rating


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'text', 'average_score']


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'text']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['article', 'score']

    def validate_score(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating score must be between 1 and 5")
        return value