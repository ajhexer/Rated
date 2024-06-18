from django.urls import path
from .views import ArticleListView, ArticleCreateView, RateArticleView

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/create/', ArticleCreateView.as_view(), name='article-create'),
    path('rate/', RateArticleView.as_view(), name='rate-article'),
]
