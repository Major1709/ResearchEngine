from pathlib import Path
import pdfplumber
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from Controller.Liste_book import list_books, filtre_books
import json

DATA_FILE = Path("./data.json")
# === Configuration ===
collection_name = "book_chunks"
qdrant_url = "http://localhost:6333"
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")

# === 1. EXTRACTION DU TEXTE ===
def extract_text_from_pdf(pdf_path, metadata_base):
    docs = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                doc = Document(
                    page_content=text,
                    metadata={
                        **metadata_base,
                        "page": page_number
                    }
                )
                docs.append(doc)
    return docs

# === 2. DÉCOUPE EN MORCEAUX ===
def split_text(text, source_info):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " "]
    )

    return splitter.split_documents([
        Document(
            page_content=f"passage: {text}",  # Pour BGE
            metadata={
                "isbn": source_info["isbn"],
                "title": source_info["title"],
                "author": source_info["author"],
                "year": source_info["year"],
                "grade": source_info["grade"],
                "domaine": source_info["domaine"]
            }
        )
    ])

def add_books(pdf_path, book, collection_name="book_chunks"):
    print(f"📘 Lecture du livre : {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    chunks = split_text(text, source_name=book)
    print(f"   → {len(chunks)} morceaux extraits.")
    client = QdrantClient(url=qdrant_url)

    # Vérifier si la collection existe déjà
    collections = client.get_collections().collections
    collection_exists = any(c.name == collection_name for c in collections)

    # === Si la collection existe, on ajoute les documents ===
    if collection_exists:
        print(f"📥 Ajout dans la collection existante : {collection_name}")
        vectorstore = Qdrant(
            client=client,
            collection_name=collection_name,
            embeddings=embeddings
        )
        vectorstore.add_documents(chunks)

    # === Sinon, on crée la collection avec les documents ===
    else:
        print(f"📁 Création de la collection : {collection_name}")
        vectorstore = Qdrant.from_documents(
            documents=chunks,
            embedding=embeddings,
            location=qdrant_url,
            collection_name=collection_name
        )

    print("✅ Opération terminée.")
    
    # Charge l'ancien contenu JSON ou crée une liste vide
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            books = json.load(f)
    else:
        books = []

    books.append(book)

    # Sauvegarde la liste mise à jour dans le fichier JSON
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

    print(f"✅ Livre ajouté à l’index : {book}")
    print(list_books())

