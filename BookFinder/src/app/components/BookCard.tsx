import { faEye, faMarker } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";



type Book = {
  title: string;
  author: string;
  year: number;
  grade: string;
  domaine: string;
  directory: string;
};
export default function BookCard({ book }: { book: Book }) {

  return (
    <div className="book-card bg-white rounded-lg shadow-md overflow-hidden transition-transform duration-300 fade-in h-full flex flex-col">
      <div className="h-48 overflow-hidden">

      </div>
      <div className="p-4 flex-1 flex flex-col">
        <div className="flex justify-between items-start mb-2">
          <h4 className="font-bold text-lg text-gray-800">{book.title}</h4>
          <span className="bg-indigo-100 text-indigo-800 text-xs px-2 py-1 rounded-full">{book.domaine}</span>
        </div>
        <p className="text-gray-600 text-sm mb-2">{book.author} ({book.year})</p>
        <div className="flex items-center mb-3">
          <span className="text-yellow-500 mr-1">{book.grade} </span>
          <span className="text-gray-500 text-sm">{book.domaine}</span>
        </div>
        <p className="text-gray-700 text-sm mb-4 flex-1">{book.directory}</p>
        <div className="flex justify-between items-center pt-3 border-t border-gray-100">
          <button className="text-indigo-600 hover:text-indigo-800 text-sm font-medium flex items-center">
            <FontAwesomeIcon icon={faMarker} className="mr-1" />
          </button>
          <button className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm px-3 py-1 rounded transition-colors flex items-center">
            <FontAwesomeIcon icon={faEye} className="mr-1" />Voir
          </button>
        </div>
      </div>
    </div>
  );
}
