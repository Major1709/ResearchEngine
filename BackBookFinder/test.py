# requirements:
# pip install sentence-transformers langchain faiss-cpu pdfplumber

import os
import pdfplumber
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

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
def split_text(text, source_name="inconnu.pdf"):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_documents([Document(page_content=text, metadata={"source": source_name})])

# === 3. EMBEDDINGS & INDEXATION ===
def create_vector_store(documents, save_path="vector_index"):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(save_path)
    print(f"\n✅ Index sauvegardé dans : {save_path}/")

# === 4. PIPELINE COMPLETE MULTI-LIVRES ===
def index_all_books(pdf_folder):
    all_chunks = []
    fichiers = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

    for fichier in fichiers:
        chemin = os.path.join(pdf_folder, fichier)
        print(f"\n📘 Traitement du fichier : {fichier}")
        texte = extract_text_from_pdf(chemin)
        morceaux = split_text(texte, source_name=fichier)
        all_chunks.extend(morceaux)
        print(f"   → {len(morceaux)} morceaux extraits.")

    print(f"\n📚 Total : {len(all_chunks)} morceaux provenant de {len(fichiers)} livres.")
    create_vector_store(all_chunks)

# === UTILISATION ===
if __name__ == "__main__":
    dossier_pdf = "/home/toma/Documents/Livre"  # Remplace par ton dossier
    index_all_books(dossier_pdf)
