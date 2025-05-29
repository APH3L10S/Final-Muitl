import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
import threading
import asyncio

from models.anime import Anime
from models.recommender import AnimeRecommender
from logic.filters import (
    filtrar_por_rating_minimo,
    filtrar_por_genero,
    ordenar_por_rating,
    obtener_rating_promedio,
    extraer_titulos,
)
from logic.async_tasks import recomendar_lenta

class AnimeApp(tk.Tk):
    def __init__(self, recommender: AnimeRecommender):
        super().__init__()
        self.title("FinalMulti - Recomendador de Anime")
        self.geometry("800x700")
        self.resizable(False, False)

        self.recommender = recommender
        self._ultimo_animes: List[Anime] = []
        self._user_id: int | None = None

        self._create_widgets()

    def _create_widgets(self) -> None:
        # Frame para entrada y botones principales
        input_frame = ttk.Frame(self)
        input_frame.pack(padx=10, pady=10, fill=tk.X)

        ttk.Label(input_frame, text="User ID:").grid(row=0, column=0, sticky=tk.W)
        self.user_entry = ttk.Entry(input_frame, width=15)
        self.user_entry.grid(row=0, column=1, sticky=tk.W)

        self.get_recs_button = ttk.Button(input_frame, text="Obtener Recomendaciones", command=self.on_get_recommendations)
        self.get_recs_button.grid(row=0, column=2, padx=10)

        # Frame para filtros y orden
        filtros_frame = ttk.LabelFrame(self, text="Filtros y Orden")
        filtros_frame.pack(padx=10, pady=10, fill=tk.X)

        # Filtro rating mínimo
        ttk.Label(filtros_frame, text="Rating mínimo:").grid(row=0, column=0, sticky=tk.W)
        self.rating_min_entry = ttk.Entry(filtros_frame, width=5)
        self.rating_min_entry.insert(0, "8.0")
        self.rating_min_entry.grid(row=0, column=1, sticky=tk.W)
        self.filter_rating_button = ttk.Button(filtros_frame, text="Filtrar por Rating", command=self.on_filter_rating)
        self.filter_rating_button.grid(row=0, column=2, padx=10)

        # Filtro por género
        ttk.Label(filtros_frame, text="Género:").grid(row=1, column=0, sticky=tk.W)
        self.genero_entry = ttk.Entry(filtros_frame, width=15)
        self.genero_entry.grid(row=1, column=1, sticky=tk.W)
        self.filter_genero_button = ttk.Button(filtros_frame, text="Filtrar por Género", command=self.on_filter_genero)
        self.filter_genero_button.grid(row=1, column=2, padx=10)

        # Ordenar
        self.sort_desc_var = tk.BooleanVar(value=True)
        self.sort_checkbox = ttk.Checkbutton(filtros_frame, text="Ordenar Descendente", variable=self.sort_desc_var)
        self.sort_checkbox.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.sort_button = ttk.Button(filtros_frame, text="Ordenar por Rating", command=self.on_ordenar_rating)
        self.sort_button.grid(row=2, column=2, padx=10)

        # Frame para resultados
        resultados_frame = ttk.LabelFrame(self, text="Resultados")
        resultados_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.results_text = tk.Text(resultados_frame, height=25, width=90, state=tk.DISABLED)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(resultados_frame, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)

        # Label para promedio rating
        self.promedio_label = ttk.Label(self, text="Rating promedio: N/A")
        self.promedio_label.pack(padx=10, pady=5)

        # Botón para recomendaciones async avanzadas
        self.async_recs_button = ttk.Button(self, text="Obtener recomendaciones avanzadas (Async)", command=self.on_async_recommendations)
        self.async_recs_button.pack(pady=5)
        self.async_recs_button.config(state=tk.DISABLED)

    def on_get_recommendations(self) -> None:
        user_id_str = self.user_entry.get().strip()
        if not user_id_str.isdigit():
            messagebox.showerror("Error", "El User ID debe ser un número entero válido.")
            return
        self._user_id = int(user_id_str)
        self._clear_results()
        self._append_text(f"Obteniendo animes mejor valorados para usuario {self._user_id}...\n")
        self.get_recs_button.config(state=tk.DISABLED)
        self.async_recs_button.config(state=tk.DISABLED)

        threading.Thread(target=self._load_recommendations_sync, daemon=True).start()

    def _load_recommendations_sync(self):
        try:
            top_animes = self.recommender.obtener_mejores_por_usuario(self._user_id, top_n=20)
            self._ultimo_animes = top_animes

            if not top_animes:
                self._append_text("No se encontraron animes para este usuario.\n")
                return

            self._append_text("Animes mejor valorados:\n")
            for a in top_animes:
                self._append_text(f"- {a.name} (Rating: {a.rating:.2f})\n")

            promedio = obtener_rating_promedio(top_animes)
            self._update_promedio(promedio)

            self.async_recs_button.config(state=tk.NORMAL)
        except Exception as e:
            self._append_text(f"Error al obtener recomendaciones: {e}\n")
        finally:
            self.get_recs_button.config(state=tk.NORMAL)

    def on_filter_rating(self) -> None:
        try:
            umbral = float(self.rating_min_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido para rating mínimo.")
            return
        filtrados = filtrar_por_rating_minimo(self._ultimo_animes, umbral)
        self._show_filtered_list(filtrados, f"Filtrado por rating mínimo ≥ {umbral}")

    def on_filter_genero(self) -> None:
        genero = self.genero_entry.get().strip()
        if not genero:
            messagebox.showerror("Error", "Ingrese un género para filtrar.")
            return
        filtrados = filtrar_por_genero(self._ultimo_animes, genero)
        self._show_filtered_list(filtrados, f"Filtrado por género: {genero}")

    def on_ordenar_rating(self) -> None:
        descendente = self.sort_desc_var.get()
        ordenados = ordenar_por_rating(self._ultimo_animes, descendente=descendente)
        self._show_filtered_list(ordenados, f"Ordenado por rating {'descendente' if descendente else 'ascendente'}")

    def _show_filtered_list(self, animes: List[Anime], titulo: str) -> None:
        self._clear_results()
        self._append_text(f"{titulo} ({len(animes)} resultados):\n")
        for a in animes:
            self._append_text(f"- {a.name} (Rating: {a.rating:.2f})\n")
        promedio = obtener_rating_promedio(animes)
        self._update_promedio(promedio)

    def _update_promedio(self, promedio: float) -> None:
        self.promedio_label.config(text=f"Rating promedio: {promedio:.2f}")

    def on_async_recommendations(self) -> None:
        if self._user_id is None:
            messagebox.showerror("Error", "Debe obtener primero recomendaciones para un usuario válido.")
            return
        self.async_recs_button.config(state=tk.DISABLED)
        self._append_text("\nObteniendo recomendaciones avanzadas asincrónicas...\n")
        asyncio.run(self._run_async_task())

    async def _run_async_task(self):
        try:
            texto = await recomendar_lenta(self._ultimo_animes)
            self._append_text(texto + "\n")
        except Exception as e:
            self._append_text(f"Error en tarea asíncrona: {e}\n")
        finally:
            self.async_recs_button.config(state=tk.NORMAL)

    def _append_text(self, texto: str) -> None:
        def inner():
            self.results_text.config(state=tk.NORMAL)
            self.results_text.insert(tk.END, texto)
            self.results_text.config(state=tk.DISABLED)
            self.results_text.see(tk.END)

        self.results_text.after(0, inner)

    def _clear_results(self) -> None:
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    # Ejemplo: ajustar rutas a tus CSVs
    recommender = AnimeRecommender("data/anime.csv", "data/ratings.csv")
    app = AnimeApp(recommender)
    app.mainloop()