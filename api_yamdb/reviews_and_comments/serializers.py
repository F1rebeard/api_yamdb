from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews_and_comments.models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        many=False,
        read_only=True,
    )

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        many=False,
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
