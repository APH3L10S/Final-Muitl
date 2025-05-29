from abc import ABC, abstractmethod
from typing import List
from models.anime import Anime

class BaseRecommender(ABC):
    """
    Clase base abstracta que define la interfaz para cualquier recomendador.
    """

    @abstractmethod
    def obtener_mejores_por_usuario(self, user_id: int, top_n: int) -> List[Anime]:
        pass

    @abstractmethod
    def recomendar_por_usuario(self, user_id: int) -> str:
        pass

    @abstractmethod
    def obtener_similares_por_genero(self, anime: Anime, limite: int) -> List[Anime]:
        pass