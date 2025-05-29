import asyncio
from typing import List
from models.anime import Anime

async def recomendar_lenta(animes: List[Anime]) -> str:
    """Simula una tarea asíncrona lenta de análisis de animes."""
    await asyncio.sleep(2)  # Simula demora externa
    if not animes:
        return "No se encontraron recomendaciones avanzadas."

    mensaje = "Recomendación avanzada basada en tus gustos:\n"
    for anime in animes[:3]:
        mensaje += f"- Tal vez te guste también '{anime.name}' (Rating: {anime.rating:.1f})\n"
    return mensaje
