from django.contrib.auth.tokens import default_token_generator
from django.http import Http404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email', 'username')
        model = User

    def validate(self, data):
        username = data['username']
        if username == 'me':
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено."
            )
        return super().validate(data)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=256)
    confirmation_code = serializers.CharField(max_length=256)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User

    def validate(self, data):
        confirmation_code = data['confirmation_code']
        username = data['username']
        if not User.objects.filter(username=username).exists():
            raise Http404
        user = User.objects.get(username=username)
        if not default_token_generator.check_token(
            user, confirmation_code
        ):
            raise serializers.ValidationError(
                'Неверный код подтверждения')
        return super().validate(data)


class CategorySerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Genre
        exclude = ['id']


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        fields = ('__all__')
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = ('__all__')


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'title_id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs['title_id']
        method = self.context.get('request').method
        if (Review.objects.filter(author=author, title=title_id).exists()
                and method == 'POST'):
            raise serializers.ValidationError('Нельзя оставлять больше одного'
                                              'отзыва!')
        return data


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'review_id', 'text', 'author', 'pub_date')
