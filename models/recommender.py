from models.anime import Anime
from models.user_rating import UserRating
from collections import defaultdict
import csv

class AnimeRecommender:
    def __init__(self, anime_path: str, ratings_path: str):
        self._anime_db = {}  # Diccionario: anime_id -> Anime
        self._user_ratings = defaultdict(list)  # Diccionario: user_id -> List[UserRating]
        self.cargar_datos_anime(anime_path)
        self.cargar_datos_ratings(ratings_path)

    def cargar_datos_anime(self, path: str):
        """Carga los datos de anime desde CSV."""
        with open(path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    anime = Anime(
                        anime_id=int(row['anime_id']),
                        name=row['name'],
                        genre=row.get('genre', ''),
                        type_=row.get('type', 'Unknown'),
                        episodes=int(row['episodes']) if row['episodes'].isdigit() else 0,
                        rating=float(row['rating']) if row['rating'] else 0.0,
                        members=int(row['members']) if row['members'] else 0
                    )
                    self._anime_db[anime.anime_id] = anime
                except Exception as e:
                    print(f"Error cargando anime: {e}")

    def cargar_datos_ratings(self, path: str):
        """Carga las valoraciones de usuarios desde CSV."""
        with open(path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    rating = UserRating(
                        user_id=int(row['user_id']),
                        anime_id=int(row['anime_id']),
                        rating=float(row['rating'])
                    )
                    if rating.es_valida():
                        self._user_ratings[rating.user_id].append(rating)
                except Exception as e:
                    print(f"Error cargando rating: {e}")

    def obtener_mejores_por_usuario(self, user_id: int, top_n: int = 5):
        """Devuelve los animes mejor valorados por un usuario."""
        ratings = self._user_ratings.get(user_id, [])
        ratings.sort(key=lambda r: r.rating, reverse=True)
        top = ratings[:top_n]
        return [self._anime_db[r.anime_id] for r in top if r.anime_id in self._anime_db]

    def obtener_similares_por_genero(self, anime: Anime, limite: int = 5):
        """Devuelve animes similares basados en géneros compartidos."""
        similares = [
            a for a in self._anime_db.values()
            if a.anime_id != anime.anime_id and any(g in a.genres for g in anime.genres)
        ]
        similares.sort(key=lambda a: a.rating, reverse=True)
        return similares[:limite]
    
    def recomendar_por_usuario(self, user_id: int, top_n: int = 5) -> str:
        """
        Genera un mensaje de recomendación personalizado para un usuario,
        basado en sus animes mejor valorados y algunos criterios.
        """
        animes_vistos = self.obtener_mejores_por_usuario(user_id, top_n=50)
        if not animes_vistos:
            return "No se encontraron datos para este usuario."

        # Promedio rating que el usuario da
        avg_rating = sum(r.rating for r in self._user_ratings[user_id]) / len(self._user_ratings[user_id])

        # Género más visto
        generos = []
        for anime in animes_vistos:
            generos.extend(anime.genres)
        from collections import Counter
        genero_comun = Counter(generos).most_common(1)[0][0] if generos else "Ninguno"

        # Animes top para recomendar
        recomendados = []
        for anime in self._anime_db.values():
            # Que no esté ya visto
            if anime in animes_vistos:
                continue
            # Que tenga el género favorito
            if genero_comun.lower() in [g.lower() for g in anime.genres]:
                recomendados.append(anime)

        recomendados.sort(key=lambda a: a.rating, reverse=True)
        recomendados_top = recomendados[:top_n]

        # Construimos el mensaje
        mensaje = f"Usuario {user_id}, tu promedio de rating es {avg_rating:.2f}.\n"
        mensaje += f"Tu género favorito es: {genero_comun}.\n"
        if recomendados_top:
            mensaje += "Te recomendamos estos animes basados en tu género favorito y calificaciones:\n"
            for a in recomendados_top:
                mensaje += f"- {a.name} (Rating: {a.rating:.2f})\n"
        else:
            mensaje += "No tenemos recomendaciones nuevas en tu género favorito por ahora.\n"

        # Consejos simples basados en rating promedio
        if avg_rating >= 8.5:
            mensaje += "\n¡Ves solo animes de alta calidad! Sigue así."
        elif avg_rating >= 7.0:
            mensaje += "\nPodrías probar explorar géneros nuevos para ampliar tus gustos."
        else:
            mensaje += "\nTe recomendamos descubrir animes mejor valorados para mejorar tu experiencia."

        return mensaje