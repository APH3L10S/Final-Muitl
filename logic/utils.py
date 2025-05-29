from typing import List, Dict, Any, Optional
import csv

def cargar_csv(ruta: str) -> List[Dict[str, Any]]:
    """
    Carga un archivo CSV y devuelve una lista de diccionarios,
    donde cada diccionario representa una fila.
    """
    with open(ruta, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)

def convertir_a_entero(valor: str, defecto: int = 0) -> int:
    """
    Convierte un string a entero de forma segura.
    Si falla, devuelve el valor por defecto.
    """
    try:
        return int(valor)
    except (ValueError, TypeError):
        return defecto

def convertir_a_decimal(valor: str, defecto: float = 0.0) -> float:
    """
    Convierte un string a flotante de forma segura.
    Si falla, devuelve el valor por defecto.
    """
    try:
        return float(valor)
    except (ValueError, TypeError):
        return defecto

def separar_generos(cadena_generos: str) -> List[str]:
    """
    Separa una cadena de géneros en una lista, manejando
    espacios y entradas vacías.
    """
    if not cadena_generos:
        return []
    return [g.strip() for g in cadena_generos.split(",") if g.strip()]

def filtrar_por_genero(animes: List[Dict[str, Any]], genero: str) -> List[Dict[str, Any]]:
    """
    Filtra una lista de animes en formato diccionario
    que contengan el género especificado.
    """
    return [
        anime for anime in animes
        if genero.lower() in map(str.lower, separar_generos(anime.get("genre", "")))
    ]

def promedio_rating(ratings: List[float]) -> Optional[float]:
    """
    Calcula el promedio de una lista de ratings.
    Devuelve None si la lista está vacía.
    """
    if not ratings:
        return None
    return sum(ratings) / len(ratings)

def truncar_texto(texto: str, longitud_max: int) -> str:
    """
    Trunca una cadena de texto si supera la longitud máxima.
    """
    if len(texto) <= longitud_max:
        return texto
    return texto[:longitud_max - 3] + "..."

def limpiar_nombre(nombre: Optional[str]) -> str:
    """
    Limpia y normaliza nombres de anime.
    """
    if not nombre:
        return ""
    return nombre.strip()
