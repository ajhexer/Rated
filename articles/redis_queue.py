import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def enqueue_article_id(article_id):
    redis_client.sadd('articles_set', article_id)


def dequeue_articles():
    article_ids = redis_client.smembers('articles_set')
    redis_client.delete('articles_set')
    return [int(article_id) for article_id in article_ids]
