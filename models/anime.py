class Anime:
    def __init__(self, anime_id: int, name: str, genre: str, type_: str, episodes: int, rating: float, members: int):
        self._anime_id = anime_id
        self._name = name
        # Separamos la cadena genre en lista de géneros
        self._genres = genre.split(', ') if genre else []
        self._type = type_
        self._episodes = episodes
        self._rating = rating
        self._members = members

    # Encapsulamiento con propiedades que respetan el dataset
    @property
    def anime_id(self):
        return self._anime_id

    @property
    def name(self):
        return self._name

    @property
    def genres(self):
        return self._genres

    @property
    def type(self):
        return self._type

    @property
    def episodes(self):
        return self._episodes

    @property
    def rating(self):
        return self._rating

    @property
    def members(self):
        return self._members

    def __str__(self):
        return f"{self._name} ({self._type}) - {', '.join(self._genres)} - Rating: {self._rating}"

    def has_genre(self, genre: str) -> bool:
        """Verifica si el anime contiene un género específico."""
        return genre.lower() in (g.lower() for g in self._genres)
