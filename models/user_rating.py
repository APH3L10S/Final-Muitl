class UserRating:
    def __init__(self, user_id: int, anime_id: int, rating: float):
        self._user_id = user_id
        self._anime_id = anime_id
        self._rating = rating

    @property
    def user_id(self):
        return self._user_id

    @property
    def anime_id(self):
        return self._anime_id

    @property
    def rating(self):
        return self._rating

    def es_valida(self) -> bool:
        """Devuelve True si el usuario asignó un rating válido (≠ -1)."""
        return self._rating != -1

    def __str__(self):
        return f"Usuario {self._user_id} valoró Anime {self._anime_id} con {self._rating}"
