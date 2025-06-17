from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama, LlamaCpp
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

prompt_template = """
Tu es un assistant intelligent spécialisé dans la recherche documentaire.

Utilise uniquement les informations contenues dans les documents ci-dessous pour répondre à la question.

Si l'information ne se trouve pas dans les documents, réponds :
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


# === Charger l'index
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("vector_index", embeddings, allow_dangerous_deserialization=True)
"""llm = LlamaCpp(
    model_path="/home/toma/Downloads/llama-3.1-8b-instruct-q4_k_m.gguf",
    n_ctx=700,
    temperature=0.7,
    top_p=0.95,
    stop=["</s>"],
    repeat_penalty=1.1,
    verbose=False,
    n_threads=8,       # adapte selon ton CPU
    max_tokens=500,
)"""
llm = Ollama(model="qwen3:8b")  # s'assure que 'llama3' est disponible dans `ollama list`

# === Construire le pipeline Q&A
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    chain_type="stuff",
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt}
)
# === Extraire tous les documents stockés
all_docs = vectorstore.docstore._dict.values()  # interne mais fonctionnel

# === Récupérer et afficher les sources uniques

# === Utilisation interactive
def search_books(query):
    
    result = qa_chain({"query": query})
    print("\n🧠 Réponse :\n", result["result"])

    # Affichage des sources
    if "Aucun information trouver." in result["result"]:
        return []
    
    sources = {doc.metadata.get("source", "inconnu") for doc in result["source_documents"]}
    print("\n📚 Livres utilisés :")
    for source in sources:
        print("•", source)
        
    return sources
