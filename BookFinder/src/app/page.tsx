// app/page.tsx
'use client';
import Header from './components/Header';
import Footer from './components/Footer';
import BookResults from './components/BookResults';
import SearchBar from './components/SearchBar';
import { useState } from 'react';
import axios from 'axios';


const sampleBooks: unknown[] | (() => unknown[]) = [];

export default function Home() {
  
  const [filtered, setFiltered] = useState(sampleBooks);
  const [loading, setLoading] = useState(false);

  const searchBooks = async (query: string) => {
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/search_books', query);
      console.log('Réponse de la recherche:', response.data);
      setFiltered(response.data);
    } catch (error) {
      console.error('Erreur lors de l’ajout du livre:', error);
    } finally {
      setLoading(false);
    }

  };
  
  return (
    <main className="bg-gradient-to-br from-indigo-50 to-purple-50 min-h-screen">
      <Header />
      
      <section className="container mx-auto px-4 py-8">
        <section className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-800 mb-4">Trouvez votre prochaine lecture</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">Découvrez des milliers de livres qui correspondent à vos goûts. Recherchez par titre, auteur ou sujet.</p>
        </section>

      <SearchBar onSearch={searchBooks} />
      {loading && <div id="loadingIndicator" className="flex justify-center items-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>}
      {!loading && <BookResults books={filtered} />}
      </section>
      <Footer />
    </main>
  );
}
