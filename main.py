import requests
import random

class RecomendacaoFilmesApp:
    def __init__(self):
        self.preferences = {}
        self.genre_mapping = {
            'acao': '28',
            'animacao': '16',
            'comedia': '35',
            'drama': '18',
            'ficcao cientifica': '878',
            'romance': '10749',
            'suspense': '53',
            'terror': '27'
        }
        self.API_KEY = 'db3922c71c7fc32d552f654d1c6cdc33'

    def get_user_preferences(self):
        for genre_name, genre_id in self.genre_mapping.items():
            rating = int(input(f"Quanto você gosta de filmes do gênero {genre_name.capitalize()}? (Digite um número de 1 a 5): "))
            self.preferences[genre_name] = rating

        self.preferences['adult_content'] = input("Você está confortável com filmes para adultos? (Sim ou Não): ").lower()
        self.preferences['violence'] = input("Você gosta de filmes com cenas violentas? (Sim ou Não): ").lower()
        self.preferences['language'] = input("Você tem preferência por filmes em um idioma específico? (Digite o idioma ou 'Qualquer'): ")

    def get_recommendations(self):
        # Obtenha recomendações com base nas preferências do usuário usando a API de filmes
        endpoint = 'https://api.themoviedb.org/3/discover/movie'
        params = {
            'api_key': self.API_KEY,
            'language': 'pt-BR',
            'sort_by': 'popularity.desc',
            'include_adult': 'false' if self.preferences['adult_content'] == 'nao' else 'true',
            'vote_average.gte': '6',
            'append_to_response': 'videos'
        }

        genre_ids = '|'.join(self.genre_mapping.values())
        params['with_genres'] = genre_ids

        if self.preferences['violence'] == 'sim':
            params['with_genres'] += '|53'

        response = requests.get(endpoint, params=params)
        data = response.json()
        return data['results']

    def show_movie_recommended(self, movie):
        print(f'Título: {movie["title"]}')
        print(f'Visão Geral: {movie["overview"]}')
        print(f'Avaliação: {movie["vote_average"]}')

    def run(self):
        print("Bem-vindo ao aplicativo de recomendação de filmes!")
        self.get_user_preferences()
        recommended_movies = self.get_recommendations()

        if recommended_movies:
            random_movie = random.choice(recommended_movies)
            self.show_movie_recommended(random_movie)
        else:
            print('Desculpe, não encontramos filmes com base nas suas preferências.')

if __name__ == '__main__':
    app = RecomendacaoFilmesApp()
    app.run()
