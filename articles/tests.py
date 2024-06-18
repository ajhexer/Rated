from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch, MagicMock
from .models import Article, Rating


class ArticleTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    @patch('articles.redis_queue.enqueue_article_id')
    @patch('django.core.cache.cache.set')
    def test_create_user(self, mock_cache_set, mock_enqueue_article_id):
        user = User.objects.create_user(username='newuser', password='newpassword')
        self.assertEqual(User.objects.count(), 2)

    @patch('articles.redis_queue.enqueue_article_id')
    @patch('django.core.cache.cache.set')
    def test_create_article(self, mock_cache_set, mock_enqueue_article_id):
        url = reverse('article-create')
        data = {'title': 'Test Article', 'text': 'This is a test article.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().title, 'Test Article')

    @patch('articles.redis_queue.enqueue_article_id')
    @patch('django.core.cache.cache.get')
    @patch('django.core.cache.cache.set')
    def test_retrieve_article(self, mock_cache_set, mock_cache_get, mock_enqueue_article_id):
        article = Article.objects.create(title='Test Article', text='This is a test article.')
        mock_cache_get.return_value = None  # Simulate cache miss

        url = reverse('article-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Test Article')

    @patch('articles.redis_queue.redis_client', new_callable=MagicMock)
    @patch('django.core.cache.cache.set')
    @patch('django.core.cache.cache.get', return_value=None)  # Simulate cache miss
    def test_create_rating(self, mock_cache_get, mock_cache_set, mock_redis_client):
        article = Article.objects.create(title='Test Article', text='This is a test article.')
        url = reverse('rate-article')
        data = {'article': article.id, 'score': 4}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.get().score, 4)
        self.assertTrue(mock_redis_client.sadd.called)
