from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama, LlamaCpp
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from Controller.Liste_book import list_books,filtre_books

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
    input_variables=["context", "question"],#tu donnes des réponses basées sur les livres indexés dans FAISS.tu ne peux pas inventer des réponses.

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
llm = Ollama(model="vicuna")  # s'assure que 'llama3' est disponible dans `ollama list`

# === Construire le pipeline Q&A
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 10}),
    chain_type="stuff",
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt}
)
# === Extraire tous les documents stockés
all_docs = vectorstore.docstore._dict.values()  # interne mais fonctionnel

# === Récupérer et afficher les sources uniques
sources = {doc.metadata.get("source", "inconnu") for doc in all_docs}
print("📚 Livres indexés dans FAISS :")
ds = filtre_books(sources, list_books())
for src in ds:
    print(src.get_title(), ":", src.get_isbn())

# === Utilisation interactive
if __name__ == "__main__":
    while True:
        query = input("❓ Question : ")
        if not query:
            break
        result = qa_chain({"query": query})
        print("\n🧠 Réponse :\n", result["result"])

        if "Aucun information trouver." in result["result"]:
            print("Aucun information trouver dans les livres indexés.")
            continue
        # Affichage des sources
        sources = {doc.metadata.get("source", "inconnu") for doc in result["source_documents"]}
        print("\n📚 Livres utilisés :")
        ds = filtre_books(sources, list_books())
        for src in ds:
            print(src.get_title())
            
    """while True:
        query = input("❓ Question : ")
        if not query:
            break

        # 🔍 Recherche avec score
        results = vectorstore.similarity_search_with_score(query, k=10)

        # 🔎 Filtrer si tu veux : ici on garde tous
        docs = [doc for doc, score in results]

        # 🤖 Génération de la réponse manuellement
        context = "\n\n".join([doc.page_content for doc in docs])
        prompt_text = f"Réponds à la question suivante en t'appuyant sur les extraits fournis.\n\nQuestion : {query}\n\nContexte :\n{context}\n\nRéponse :"
        reponse = llm.invoke(prompt_text)

        print("\n🧠 Réponse :\n", reponse)

        # 📚 Sources + scores
        print("\n📚 Sources utilisées :")
        for doc, score in results:
            nom = doc.metadata.get("source", "inconnu")
            print(f"- {nom} (score: {1 - score:.2f})")"""