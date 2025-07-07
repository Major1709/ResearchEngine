from Controller.Add_RAG_Data import add_books

data = {
    "isbn": "978-0-06-0050-4",
    "title": "Système de recommandation par filtrage Collaboratif",
    "author": "BAHLOULI ACHRAF",
    "year": 2020,
    "grade": "M2",
    "domaine": "INFORMATIQUE",
    "directory": "/home/toma/Téléchargements/Mémoire.pdf.pdf"
}
add_books(data['directory'], data)
