from models.anime import Anime
from typing import List, Dict
from collections import defaultdict
from functools import reduce

def contar_animes_por_genero(animes: List[Anime]) -> Dict[str, int]:
    """Cuenta cuántos animes hay por género."""
    conteo_generos = defaultdict(int)
    for anime in animes:
        for genero in anime.genres:  # Cambio aquí
            conteo_generos[genero.strip().lower()] += 1
    return dict(conteo_generos)

def promedio_rating_por_tipo(animes: List[Anime]) -> Dict[str, float]:
    """Devuelve el promedio de rating por tipo de anime (TV, Movie, OVA, etc)."""
    totales_por_tipo = defaultdict(lambda: {'suma': 0.0, 'cantidad': 0})
    for anime in animes:
        tipo = anime.type.strip()  # Cambio aquí
        totales_por_tipo[tipo]['suma'] += anime.rating
        totales_por_tipo[tipo]['cantidad'] += 1

    return {
        tipo: round(datos['suma'] / datos['cantidad'], 2)
        for tipo, datos in totales_por_tipo.items() if datos['cantidad'] > 0
    }

def genero_mas_comun(animes: List[Anime]) -> str:
    """Devuelve el género más común entre una lista de animes."""
    frecuencias = contar_animes_por_genero(animes)
    return max(frecuencias.items(), key=lambda item: item[1])[0] if frecuencias else ""

def total_episodios(animes: List[Anime]) -> int:
    """Devuelve el total de episodios sumando todos los animes."""
    return reduce(lambda acc, anime: acc + anime.episodes, animes, 0)  # Cambio aquí
