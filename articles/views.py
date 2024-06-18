from .models import Article, Rating
from .serializers import ArticleSerializer, RatingSerializer, ArticleCreateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .pagination import ArticlePagination
from rest_framework import generics, status
from django.core.cache import cache
from articles.redis_queue import enqueue_article_id


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all().order_by('id')
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination

    def get_queryset(self):
        articles = cache.get('articles')
        if not articles:
            articles = Article.objects.all().order_by('id')
            cache.set('articles', articles, timeout=60)
        return articles


class ArticleCreateView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer


class RateArticleView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        article = request.data.get('article')
        score = int(request.data.get('score'))
        article = Article.objects.get(pk=article)
        rating, _ = Rating.objects.update_or_create(
            user=user,
            article=article,
            defaults={'score': score}
        )
        enqueue_article_id(rating.article.id)
        return Response({'message': 'Rating submitted successfully'}, status=status.HTTP_200_OK)