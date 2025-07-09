from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_mistralai import ChatMistralAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.docstore.in_memory import InMemoryDocstore
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant


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

def load_qdrant_vector_store(
    collection_name: str,
    embeddings,
    host: str = "localhost",
    port: int = 6333,
) -> Qdrant:
    # Connexion au client Qdrant
    client = QdrantClient(
        host=host,
        port=port,
    )

    # Vérifie si la collection existe
    if not client.collection_exists(collection_name):
        raise ValueError(f"❌ La collection '{collection_name}' n'existe pas dans Qdrant.")

    # Charge la vectorstore LangChain basée sur Qdrant
    vectorstore = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings,
    )

    return vectorstore


# === Charger l'index
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
vectorstore = load_qdrant_vector_store("book_chunks", embeddings)

# === Construire le pipeline Q&A
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_type="mmr",
    search_kwargs={"k": 7, "fetch_k": 17, "lambda_mult": 0.5},),
    chain_type="map_reduce",
    return_source_documents=True,
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
