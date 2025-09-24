# 🎬 Movie Reviews Project

A Django-based movie recommendation system that uses OpenAI embeddings and cosine similarity to suggest movies based on user descriptions.

## Features

- **Movie Database**: Browse and search through a collection of movies
- **AI-Powered Recommendations**: Get movie suggestions using semantic similarity
- **Statistics Dashboard**: View charts of movies by year and genre
- **News Section**: Stay updated with movie-related news
- **Image Generation**: Automatically generate movie posters using DALL-E

## Tech Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite
- **AI Integration**: OpenAI API (GPT-3.5, DALL-E, Embeddings)
- **Frontend**: Bootstrap 5.3.7
- **Charts**: Matplotlib
- **Environment**: Python 3.13

## Quick Start

### Prerequisites
- Python 3.13+
- OpenAI API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd moviereviewsproject
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create `openAI.env` file:
   ```
   openai_apikey=your_openai_api_key_here
   ```

4. **Database setup**
   ```bash
   python manage.py migrate
   python manage.py add_movies_db
   ```

5. **Generate embeddings (required for recommendations)**
   ```bash
   python manage.py movie_embeddings
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000` to start exploring!

## 📊 Management Commands

| Command | Description |
|---------|-------------|
| `add_movies_db` | Load initial movie data from JSON |
| `movie_embeddings` | Generate embeddings for all movies |
| `update_descriptions` | Update movie descriptions using AI |
| `update_images` | Generate movie posters with DALL-E |
| `count_embeddings` | Check how many movies have embeddings |

## Key Pages

- **Home** (`/`): Browse and search movies
- **Recommend** (`/recommend/`): AI-powered movie recommendations
- **Statistics** (`/statistics/`): Visual charts and analytics
- **News** (`/news/`): Latest movie news

## How Recommendations Work

1. User enters a movie description (e.g., "fairy godmother movie")
2. System generates embedding for the user's prompt using OpenAI
3. Calculates cosine similarity with all movie embeddings in database
4. Returns top 5 most similar movies with similarity scores

## 👥 Author

© 2025 - Mariana Carrasquilla Botero

## License

This project is for educational purposes.
