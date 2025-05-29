from ui.interface import AnimeApp
from models.recommender import AnimeRecommender

def main():
    try:
        recomendador = AnimeRecommender("data/anime.csv", "data/rating.csv")
    except FileNotFoundError as e:
        print(f"No se pudo cargar los datos: {e}")
        return

    app = AnimeApp(recomendador)
    app.mainloop()

if __name__ == "__main__":
    main()