'use client';

import { faLongArrowRight, faSearch} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

export default function SearchBar({ onSearch }: { onSearch: (query: string) => void }) {
  return (
        <section className="max-w-3xl mx-auto mb-16 bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow duration-300">
            <div className="relative">
                <FontAwesomeIcon icon={faSearch} className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input 
                    type="text" 
                    id="bookSearch" 
                    placeholder="Rechercher des livres (ex. Harry Potter, Stephen King, Fantasy...)" 
                    className="w-full pl-12 pr-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-gray-700"
                    onKeyDown={(e) => {
                    if (e.key === "Enter") onSearch((e.target as HTMLInputElement).value);
                    }}
                />
                <button 
                    id="searchBtn"
                    className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-1.5 rounded-md transition-colors duration-300 flex items-center"
                    onClick={() => {
                    const input = document.querySelector('input') as HTMLInputElement;
                    onSearch(input?.value || '');
                    }}
                >
                    <span className="hidden sm:inline">Rechercher</span>
                    <FontAwesomeIcon icon={faLongArrowRight} className="fas fa-arrow-right ml-2" />
                </button>
            </div>
            <div className="flex flex-wrap gap-2 mt-4 justify-center">
                <button className="tag-btn bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm hover:bg-indigo-200 transition-colors">Fantasy</button>
                <button className="tag-btn bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm hover:bg-blue-200 transition-colors">Science-fiction</button>
                <button className="tag-btn bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm hover:bg-green-200 transition-colors">Biographie</button>
                <button className="tag-btn bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm hover:bg-purple-200 transition-colors">Romance</button>
                <button className="tag-btn bg-yellow-100 text-yellow-700 px-3 py-1 rounded-full text-sm hover:bg-yellow-200 transition-colors">Historique</button>
            </div>
        </section>
  );
}
