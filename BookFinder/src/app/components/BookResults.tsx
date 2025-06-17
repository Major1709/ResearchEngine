'use client';

import BookCard from "./BookCard";

type Book = {
  title: string;
  author: string;
  year: number;
  grade: string;
  domaine: string;
  directory: string;
};

export default function BookResults({ books }: { books: Book[] }) {
  if (!books.length) {
    return<div id="emptyState" className="text-center py-12">
            <div className="max-w-md mx-auto">
                <i className="fas fa-book-open text-6xl text-gray-300 mb-4"></i>
                <h3 className="text-xl font-medium text-gray-600 mb-2">Aucune recherche effectuée</h3>
                <p className="text-gray-500">Entrez un terme de recherche pour découvrir des livres passionnants</p>
            </div>
        </div>
  }
  return (
        <section id="resultsSection">
            <div className="flex justify-between items-center mb-6">
                <h3 className="text-2xl font-semibold text-gray-800">Résultats de votre recherche</h3>
                <div className="flex items-center">
                    <span className="text-gray-600 mr-2">Trier par:</span>
                    <select className="bg-white border border-gray-300 rounded-md px-3 py-1 text-gray-700 focus:outline-none focus:ring-1 focus:ring-indigo-500">
                        <option>Pertinence</option>
                        <option>Plus récents</option>
                        <option>Meilleures notes</option>
                    </select>
                </div>
            </div>

            <div id="bookResults" className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {books.map((book, idx) => (
                    console.log(books),
                    <BookCard key={idx} book={book} />
                ))}
            </div>
        </section>
  );
}
    
