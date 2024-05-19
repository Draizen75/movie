from flask import Flask, render_template, request
import requests

app = Flask(__name__)
TMDB_API_KEY = 'cb20ec49659b412618f1a6d5c816ce20'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        return search_movie(movie_name)
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Fetch total number of movies
    total_movies_url = f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=en-US'
    total_movies_response = requests.get(total_movies_url)
    total_movies_data = total_movies_response.json()
    total_movies = total_movies_data['total_results']

    # Fetch average rating of movies
    top_rated_url = f'https://api.themoviedb.org/3/movie/top_rated?api_key={TMDB_API_KEY}&language=en-US'
    top_rated_response = requests.get(top_rated_url)
    top_rated_data = top_rated_response.json()
    top_rated_movies = top_rated_data['results']
    average_rating = sum(movie['vote_average'] for movie in top_rated_movies) / len(top_rated_movies)

    return render_template('dashboard.html', total_movies=total_movies, average_rating=average_rating)

def search_movie(movie_name):
    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}'
    response = requests.get(search_url)
    data = response.json()
    if data['results']:
        movie = data['results'][0]  # Taking the first result for simplicity
        movie_id = movie['id']
        movie_details = get_movie_details(movie_id)
        recommendations = get_recommendations(movie_id)
        return render_template('movie.html', movie=movie_details, recommendations=recommendations)
    return render_template('index.html', error='Movie not found')

def get_movie_details(movie_id):
    details_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}'
    response = requests.get(details_url)
    movie = response.json()
    movie['poster_path'] = movie['poster_path'] if movie['poster_path'] else '/default_poster.png'
    return movie

def get_recommendations(movie_id):
    recommendations_url = f'https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}'
    response = requests.get(recommendations_url)
    recommendations = response.json().get('results', [])
    for rec in recommendations:
        rec['poster_path'] = rec['poster_path'] if rec['poster_path'] else '/default_poster.png'
    return recommendations

if __name__ == '__main__':
    app.run(debug=True)
