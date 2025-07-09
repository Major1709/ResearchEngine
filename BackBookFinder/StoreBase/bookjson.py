import json
import pdfplumber
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from qdrant_client import QdrantClient

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

# === 3. EMBEDDINGS + INDEXATION QDRANT ===
def create_qdrant_index(documents, collection_name="book_chunks"):
    print("📡 Connexion à Qdrant...")
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
    
    client = QdrantClient(path="qdrant_data")  # pour stockage local (fichiers)
    Qdrant.from_documents(
        documents,
        embedding=embeddings,
        collection_name=collection_name,
        url="http://localhost:6333",
        force_recreate=True,
        prefer_grpc=True
    )

    print(f"✅ Index Qdrant créé avec {len(documents)} chunks dans la collection '{collection_name}'.")

# === 4. PIPELINE COMPLETE MULTI-LIVRES ===
def index_all_books_qdrant(books, collection_name="book_chunks"):
    all_chunks = []
    print("📚 Indexation de plusieurs livres :\n")
    for book in books:
        texte = extract_text_from_pdf(book["directory"], book)
        morceaux = split_text(texte, source_info=book)
        all_chunks.extend(morceaux)
        print(f" → {len(morceaux)} morceaux extraits de : {book['title']} ({book['isbn']})")
        print("-" * 50)

    print(f"\n📚 Total : {len(all_chunks)} morceaux pour {len(books)} livres.")
    create_qdrant_index(all_chunks, collection_name=collection_name)


# === UTILISATION ===
if __name__ == "__main__":
    # Charger le fichier JSON
    with open("/home/toma/Documents/BackBookFinder/data.json", "r", encoding="utf-8") as f:
        books = json.load(f)
    index_all_books_qdrant(books)
