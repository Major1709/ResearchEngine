import json
import pdfplumber
import faiss
import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.docstore.in_memory import InMemoryDocstore
import os
import pickle


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

# === 3. EMBEDDINGS & INDEXATION ===

def create_vector_store(documents, save_path="vector_index_bge_hnsw"):
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")

    # Préfixe passage:
    for doc in documents:
        doc.page_content = f"passage: {doc.page_content}"

    # Embeddings
    vectors = embeddings.embed_documents([doc.page_content for doc in documents])
    vectors = np.array(vectors).astype('float32')
    dim = vectors.shape[1]

    # HNSW + IDMAP pour gérer les IDs explicitement
    hnsw = faiss.IndexHNSWFlat(dim, 32)
    hnsw.hnsw.efConstruction = 200
    hnsw.hnsw.efSearch = 50
    index = faiss.IndexIDMap(hnsw)

    ids = np.arange(len(documents)).astype(np.int64)
    index.add_with_ids(vectors, ids)

    # Mapping LangChain
    index_to_docstore_id = {int(i): str(i) for i in ids}
    docstore = InMemoryDocstore({str(i): doc for i, doc in zip(ids, documents)})

    vectorstore = FAISS(index, embeddings, index_to_docstore_id, docstore)

    # Crée le dossier si inexistant
    os.makedirs(save_path, exist_ok=True)

    # Sauvegarde FAISS
    faiss.write_index(index, os.path.join(save_path, "index.faiss"))

    # Sauvegarde docstore
    with open(os.path.join(save_path, "docstore.pkl"), "wb") as f:
        pickle.dump(dict(docstore._dict), f)

    # Sauvegarde index_to_docstore_id
    with open(os.path.join(save_path, "index_to_docstore_id.json"), "w") as f:
        json.dump(index_to_docstore_id, f)

    print(f"\n✅ Index HNSW + metadata sauvegardés dans : {save_path}/")

# === 4. PIPELINE COMPLETE MULTI-LIVRES ===
def index_all_books(books):
    all_chunks = []
    print("📚 Liste des livres :\n")
    for book in books:
        texte = extract_text_from_pdf(book['directory'])
        morceaux = split_text(texte, source_name=book)
        all_chunks.extend(morceaux)
        print(f"   → {len(morceaux)} morceaux extraits. de {book['title']} ({book['isbn']})")
        print("-" * 50)

    print(f"\n📚 Total : {len(all_chunks)} livres.")
    create_vector_store(all_chunks)

# === UTILISATION ===
if __name__ == "__main__":
    # Charger le fichier JSON
    with open("/home/toma/Documents/BackBookFinder/data.json", "r", encoding="utf-8") as f:
        books = json.load(f)
    index_all_books(books)
