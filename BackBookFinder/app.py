# main.py
import json
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from Controller.Liste_book import list_books, filtre_books
from Controller.Search_book import search_books
from test3 import add_books

app = FastAPI()

# Autoriser le frontend à communiquer avec FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # le port de Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
DATA_FILE = Path("/home/toma/Documents/projet pres/data.json")

@app.post("/search_books")
async def add_book(request: Request):
    text = await request.body()
    book = search_books(text.decode('utf-8'))
    results = filtre_books(book, list_books())
    return results


@app.post("/uploadfile")
async def upload_book(
    isbn: str = Form(...),
    title: str = Form(...),
    author: str = Form(...),
    year: int = Form(...),
    grade: str = Form(...),
    domaine: str = Form(...),
    directory: UploadFile = File(...)
):
    # Crée dossier uploads s'il n'existe pas
    upload_dir = Path("/home/toma/Documents/projet pres/upload")
    upload_dir.mkdir(exist_ok=True)

    # Sauvegarde le fichier uploadé
    file_location = upload_dir / directory.filename
    contents = await directory.read()
    with open(file_location, "wb") as f:
        f.write(contents)

    # Charge l'ancien contenu JSON ou crée une liste vide
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            books = json.load(f)
    else:
        books = []

    # Prépare la nouvelle entrée (avec chemin relatif du fichier)
    new_book = {
        "isbn": isbn,
        "title": title,
        "author": author,
        "year": year,
        "grade": grade,
        "domaine": domaine,
        "directory": str(file_location)
    }

    # Ajoute la nouvelle entrée
    add_books(str(file_location), isbn)  # Indexe le livre
    books.append(new_book)

    # Sauvegarde la liste mise à jour dans le fichier JSON
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

    return {"message": "Livre ajouté avec succès", "book": new_book}