from celery import shared_task
from .models import Article, Rating
import numpy as np


@shared_task
def process_articles():
    from .redis_queue import dequeue_articles
    articles = dequeue_articles()

    for article in articles:
        update_article_ratings.apply_async(args=[article])


@shared_task
def update_article_ratings(article_id):
    article = Article.objects.get(pk=article_id)
    ratings = Rating.objects.filter(article=article).values_list('score', flat=True)
    if ratings:
        scores = np.array(list(ratings))
        new_average = np.mean(scores)
        new_std_deviation = np.std(scores)
        if abs(new_average - article.average_score) > 2 * new_std_deviation:
            article.number_of_ratings = len(scores)
        else:
            article.average_score = new_average
            article.standard_deviation = new_std_deviation
            article.number_of_ratings = len(scores)

        article.save()


