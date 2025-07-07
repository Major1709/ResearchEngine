from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_mistralai import ChatMistralAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
import faiss
import json
import pickle
from langchain_community.docstore.in_memory import InMemoryDocstore

llm = ChatMistralAI(api_key="1gup54p92G4fK7FkyspPGsCoM4QUi2jO", model="mistral-medium", temperature=0.1)
#llm = OllamaLLM(model="qwen3:8b",n_threads=8,temperature=0.5)  # s'assure que 'llama3' est disponible dans `ollama list`

prompt_template = """
Tu es un assistant intelligent spécialisé dans la recommandation documentaire, livre et de memoire.

a partir de chaque context resume se que tu a trouver sans reprendre les passage des documents.

Si aucun des information dans les documents ne concerne pas au context de sujet souhaité réponds :
"Aucun information trouver."

----------------
{context}
----------------

Question : {question}
Réponse :
"""
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
)

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


# === Charger l'index
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
vectorstore = load_vector_store("vector_index_bge_hnsw", embeddings)

# === Construire le pipeline Q&A
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 20}),
    chain_type="stuff",
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt}
)

# === Utilisation interactive
def search_books(query):
    
    result = qa_chain.invoke({"query": query})
    print("\n🧠 Réponse :\n", result["result"])

    # Affichage des sources
    if "Aucun information trouver." in result["result"]:
        return []
    
    sources = {doc.metadata.get("isbn", "Inconnu") for doc in result["source_documents"]}
    print("\n📚 Livres utilisés :")
    for source in sources:
        print("•", source)
        
    return sources
