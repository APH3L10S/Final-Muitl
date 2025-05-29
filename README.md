
# 🎌 FinalMulti - Recomendador de Anime

**FinalMulti** es una aplicación de escritorio escrita en Python que recomienda animes a partir de un dataset de puntuaciones de usuarios. Utiliza una interfaz gráfica (Tkinter) y aplica múltiples paradigmas de programación: orientado a objetos, funcional y concurrente.

---

## 🧠 Características

- 📊 Filtrado por género y por rating mínimo
- 🔀 Ordenamiento ascendente/descendente por rating
- 🎭 Recomendaciones personalizadas por ID de usuario
- 🧵 Recomendaciones avanzadas asincrónicas sin bloquear la interfaz
- 📈 Cálculo del rating promedio dinámicamente

---

## ⚙️ Requisitos

- Python 3.10 o superior
- Sistemas operativos compatibles: Windows, macOS, Linux

### 📦 Instalación de dependencias

```bash
pip install -r requirements.txt
````

Si no tienes `pip`, puedes instalarlo siguiendo [estas instrucciones](https://pip.pypa.io/en/stable/installation/).

---

## 📂 Estructura del Proyecto

```
FinalMulti/
├── main.py
├── data/
│   ├── anime.csv
│   └── rating.csv
├── models/
│   ├── __init__.py
│   ├── anime.py
│   ├── user_rating.py
|   ├── base_recommender.py
│   └── recommender.py
├── logic/
│   ├── __init__.py
│   ├── filters.py
|   ├── async_tasks.py
│   ├── aggregator.py
│   └── utils.py
├── ui/
│   └── interface.py
├── .env
├── requirements.txt
└── README.md
```

---

## 🚀 Ejecución del programa

Para iniciar la aplicación, asegúrate de tener los archivos `anime.csv` y `ratings.csv` en la carpeta `data/`, y luego ejecuta:

```bash
python main.py
```

Esto abrirá la interfaz gráfica desde donde puedes:

* Ingresar un **ID de usuario**
* Aplicar filtros y ordenar los resultados
* Ejecutar recomendaciones asincrónicas avanzadas

---

## 🧪 Dataset utilizado

* **anime.csv**: contiene la información de los animes (nombre, géneros, etc.)
* **ratings.csv**: contiene las valoraciones dadas por los usuarios a distintos animes

Ambos archivos se deben colocar en la carpeta `data/`.

---

## ✨ Paradigmas de Programación Aplicados

* **Programación Orientada a Objetos:** usada para modelar las clases `anime` y `user_rating`.
* **Programación Funcional:** filtros, transformaciones y operaciones con `map`, `filter`, `reduce`.
* **Programación Concurrente (Asincronía):** se usa `asyncio` para ejecutar recomendaciones avanzadas sin bloquear la interfaz.

---

## 🎥 Videos

- 📹 [Demo de la App](https://drive.google.com/file/d/1IAGdNurTMg_2mLvSoMizgL9rXNMb-Koh/view?usp=sharing)
- 📹 [Presentacion Tecnica](https://drive.google.com/file/d/1xOI6vgmHjmlyJR0ju6mj5KTF888dSvHS/view?usp=sharing)