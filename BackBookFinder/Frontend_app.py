# main.py
import json
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from Controller.Liste_book import list_books, filtre_books
from Controller.Search_book import search_books
from Controller.Add_RAG_Data import add_books

app = FastAPI()

# Autoriser le frontend à communiquer avec FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # le port de Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    upload_dir = Path("./BackBookFinder/upload")
    upload_dir.mkdir(exist_ok=True)

    # Sauvegarde le fichier uploadé
    file_location = upload_dir / directory.filename
    contents = await directory.read()
    with open(file_location, "wb") as f:
        f.write(contents)



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

    return {"message": "Livre ajouté avec succès", "book": new_book}


#uvicorn Frontend_app:app --reload