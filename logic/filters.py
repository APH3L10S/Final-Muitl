from models.anime import Anime
from typing import List
from functools import reduce

def filtrar_por_rating_minimo(animes: List[Anime], umbral: float) -> List[Anime]:
    """Filtra los animes que tienen rating mayor o igual al umbral."""
    return list(filter(lambda a: a.rating >= umbral, animes))

def filtrar_por_genero(animes: List[Anime], genero: str) -> List[Anime]:
    """Filtra los animes que contienen el género especificado."""
    return list(filter(lambda a: genero.lower() in [g.lower() for g in a.genres], animes))

def ordenar_por_rating(animes: List[Anime], descendente: bool = True) -> List[Anime]:
    """Ordena los animes por rating."""
    return sorted(animes, key=lambda a: a.rating, reverse=descendente)

def obtener_rating_promedio(animes: List[Anime]) -> float:
    """Devuelve el promedio del rating de una lista de animes."""
    if not animes:
        return 0.0
    total = reduce(lambda acc, a: acc + a.rating, animes, 0.0)
    return total / len(animes)

def extraer_titulos(animes: List[Anime]) -> List[str]:
    """Devuelve una lista de nombres de animes."""
    return list(map(lambda a: a.name, animes))
