import os
import pdfplumber
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from Controller.Liste_book import list_books, filtre_books

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

def add_books(pdf_path,book_isbn, index_path="vector_index"):
    # 1. Lire et découper le texte
    print(f"📘 Lecture du livre : {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    chunks = split_text(text, source_name=book_isbn)

    print(f"   → {len(chunks)} morceaux extraits.")

    # 2. Créer ou charger l'index
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    if os.path.exists(index_path):
        print("📂 Chargement de l'index existant...")
        vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

        print("→ Dimensions de l’index FAISS :", vectorstore.index.d)
        sample_embedding = embeddings.embed_query("test")
        print("→ Dimensions des embeddings générés :", len(sample_embedding))
        vectorstore.add_documents(chunks)
    else:
        print("📁 Création d’un nouvel index...")
        vectorstore = FAISS.from_documents(chunks, embeddings)

    # 3. Sauvegarde
    vectorstore.save_local(index_path)
    print(f"✅ Livre ajouté à l’index : {book_isbn}")
    print(list_books())
