from media import Media
from fresh_tomatoes import *

# Create a list of movies
movies = []
movie = Media(
    "Pacific Rim 2",
    "http://image.phimmoi.net/film/6129/poster.medium.jpg",
    "https://youtu.be/US7lYhgEuhE"
)
movies.append(movie)
movie = Media(
    "Dead Pool",
    "http://image.phimmoi.net/film/5001/poster.medium.jpg",
    "https://youtu.be/Z5ezsReZcxU"
)
movies.append(movie)

# Generate the movie list HTML page and open it on web browser
open_movies_page(movies)
