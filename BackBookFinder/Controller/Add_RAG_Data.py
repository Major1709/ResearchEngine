import os
from pathlib import Path
import pdfplumber
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from Controller.Liste_book import list_books, filtre_books
import faiss
import json
import pickle
from langchain_community.docstore.in_memory import InMemoryDocstore
import numpy as np

DATA_FILE = Path("./data.json")
# === 1. EXTRACTION DU TEXTE ===
def extract_text_from_pdf(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text

# === 2. DÉCOUPE EN MORCEAUX ===
def split_text(text, source_name):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,  # Plus grand chunk (≈300 tokens)
        chunk_overlap=200,  # Plus grand overlap car plus gros chunk
        separators=["\n\n", "\n", ".", " "]
    )

    return splitter.split_documents([
        Document(
            page_content=text,
            metadata={
                "isbn": source_name['isbn'],
                "title": source_name['title'],
                "author": source_name['author'],
                "year": source_name['year'],
                "grade": source_name['grade'],
                "domaine": source_name['domaine']
            }
        )
    ])

def load_vector_store(save_path, embeddings):
    # Charge FAISS index
    index = faiss.read_index(os.path.join(save_path, "index.faiss"))

    # Charge docstore
    with open(os.path.join(save_path, "docstore.pkl"), "rb") as f:
        doc_dict = pickle.load(f)
    docstore = InMemoryDocstore(doc_dict)

    # Charge index_to_docstore_id et convertit les clés en int
    with open(os.path.join(save_path, "index_to_docstore_id.json"), "r") as f:
        raw_mapping = json.load(f)
    index_to_docstore_id = {int(k): v for k, v in raw_mapping.items()}

    # Reconstruit vectorstore
    vectorstore = FAISS(
        index=index,
        embedding_function=embeddings,
        index_to_docstore_id=index_to_docstore_id,
        docstore=docstore
    )

    return vectorstore

def add_books(pdf_path, book, index_path="vector_index_bge_hnsw"):
    print(f"📘 Lecture du livre : {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    chunks = split_text(text, source_name=book)
    print(f"   → {len(chunks)} morceaux extraits.")

    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
    for chunk in chunks:
        chunk.page_content = f"passage: {chunk.page_content}"

    if os.path.exists(index_path):
        print("📂 Chargement de l'index existant...")
        vectorstore = load_vector_store(index_path, embeddings)

        # Générer les embeddings
        new_vectors = embeddings.embed_documents([c.page_content for c in chunks])
        new_vectors_np = np.array(new_vectors).astype('float32')

        # Générer des IDs uniques
        current_max_id = max(map(int, vectorstore.index_to_docstore_id.keys()), default=-1)
        new_ids = [current_max_id + 1 + i for i in range(len(chunks))]
        new_ids_np = np.array(new_ids).astype('int64')

        # Ajout avec IDs explicites
        vectorstore.index.add_with_ids(new_vectors_np, new_ids_np)

        # Mise à jour des mappings
        for i, chunk in zip(new_ids, chunks):
            vectorstore.index_to_docstore_id[i] = str(i)
            vectorstore.docstore._dict[str(i)] = chunk

    else:
        print("📁 Création d’un nouvel index...")
        dim = len(embeddings.embed_query("passage: test"))
        base_index = faiss.IndexHNSWFlat(dim, 32)
        base_index.hnsw.efConstruction = 200
        base_index.hnsw.efSearch = 50

        index = faiss.IndexIDMap(base_index)

        vectors = embeddings.embed_documents([c.page_content for c in chunks])
        vectors_np = np.array(vectors).astype('float32')
        ids_np = np.arange(len(chunks)).astype('int64')

        index.add_with_ids(vectors_np, ids_np)

        index_to_docstore_id = {i: str(i) for i in range(len(chunks))}
        docstore = InMemoryDocstore({str(i): c for i, c in enumerate(chunks)})

        vectorstore = FAISS(index, embeddings, index_to_docstore_id, docstore)

    # Sauvegarde
    os.makedirs(index_path, exist_ok=True)
    faiss.write_index(vectorstore.index, os.path.join(index_path, "index.faiss"))

    with open(os.path.join(index_path, "docstore.pkl"), "wb") as f:
        pickle.dump(dict(vectorstore.docstore._dict), f)

    with open(os.path.join(index_path, "index_to_docstore_id.json"), "w") as f:
        json.dump({int(k): v for k, v in vectorstore.index_to_docstore_id.items()}, f)
    
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

