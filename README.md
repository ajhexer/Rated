
# Article Project

## Description

The Article Project is designed to handle and process article ratings using Django as the web framework. This project includes functionalities for user authentication, article management, and implementing a rate validation system to handle unrealistic rates using standard deviation.

## Features

- **User Authentication**: Built-in support for user registration, login, and token-based authentication using Django and Djoser.
- **Rate Validation**: A sophisticated method to handle unrealistic rates using standard deviation.

## Rate Handling Using Standard Deviation

To manage unrealistic rates, we employ a statistical approach based on standard deviation. Here's a brief overview of the method:

1. **Data Collection**: Collect a series of rate values.
2. **Calculate Mean**: Compute the mean (average) of the rate values.
3. **Calculate Standard Deviation**: Compute the standard deviation of the rate values.
4. **Detection Logic**: Define a rate as unrealistic if it deviates significantly from the mean (e.g., more than 2 standard deviations).

This method helps in identifying and mitigating outliers in rate values effectively.

### Example Implementation Snippet

```python
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
```

## Deployment Using Docker Compose

To deploy the Article project using Docker Compose, follow these steps:

1. **Navigate to Deployments Directory**

    ```bash
    cd deployments
    ```

2. **Build and Start Containers**

    Use the following command to build and start the Docker containers:

    ```bash
    docker-compose up --build
    ```

3. **Access the Application**

    Once the containers are up and running, you can access the application at `http://localhost:8000`.

## Sending Sample Requests Using `curl`

To interact with the API, you can use `curl` to send sample requests. Here are some example commands:

### Register a New User

```bash
curl -X POST http://localhost:8000/api/auth/users/ \
    -H "Content-Type: application/json" \
    -d '{"username": "sampleuser", "password": "samplepassword"}'
```

### Login and Obtain Token

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
    -H "Content-Type: application/json" \
    -d '{"username": "sampleuser", "password": "samplepassword"}'
```

### Create a New Article

```bash
curl -X POST http://localhost:8000/api/articles/ \
    -H "Authorization: Token <your_token>" \
    -H "Content-Type: application/json" \
    -d '{"title": "Sample Article", "content": "This is a sample article."}'
```

### Get List of Articles

```bash
curl -X GET http://localhost:8000/api/articles/ \
    -H "Authorization: Token <your_token>"
```

