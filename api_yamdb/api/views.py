from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.mixins import AccessMixin
from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                             ReviewCommentPermissions)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignUpSerializer, TitleReadSerializer,
                             TitleWriteSerializer, TokenSerializer,
                             UserMeSerializer, UserSerializer)
from reviews.models import Category, Comment, Genre, Review, Title, User


class GetUpdateViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'], url_path='me',
            permission_classes=[IsAuthenticated])
    def get_object_me(self, request):
        user_me = get_object_or_404(User, username=request.user.username)
        if request.method == 'PATCH':
            serializer = UserMeSerializer(user_me, data=request.data,
                                          partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserMeSerializer(user_me)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpAPI(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(
            User, username=serializer.data.get('username')
        )
        email = user.email
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения',
            f'Код подтверждения: {confirmation_code}',
            settings.EMAIL_HOST_USER,
            [f'{email}']
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAPI(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(
            username=serializer.data.get('username')
        )
        refresh = RefreshToken.for_user(user)
        data = {
            'token': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score")).all()
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer

        return TitleWriteSerializer


class CategoryViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']
    lookup_field = 'slug'


class ReviewViewSet(AccessMixin):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [ReviewCommentPermissions, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))

        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        queryset = Review.objects.filter(title__id=self.kwargs.get('title_id'))

        return queryset


class CommentViewSet(AccessMixin):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title__id=title_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        queryset = Comment.objects.filter(
            review__id=self.kwargs.get('review_id')
        )
        return queryset
