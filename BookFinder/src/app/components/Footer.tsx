'use client';
import { faBook} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

export default function Header() {
  return (
    <footer className="bg-white border-t border-gray-200 py-8 mt-12">
        <div className="container mx-auto px-4">
            <div className="flex flex-col md:flex-row justify-between items-center">
                <div className="mb-4 md:mb-0">
                    <div className="flex items-center">
                        <FontAwesomeIcon icon={faBook} className="open text-2xl text-indigo-600 mr-2" />
                        <span className="text-lg font-semibold">BookFinder</span>
                    </div>
                    <p className="text-gray-500 text-sm mt-1">Votre compagnon de lecture depuis 2023</p>
                </div>
                <div className="flex space-x-6">
                    <a href="#" className="text-gray-600 hover:text-indigo-600"><i className="fab fa-twitter"></i></a>
                    <a href="#" className="text-gray-600 hover:text-indigo-600"><i className="fab fa-facebook"></i></a>
                    <a href="#" className="text-gray-600 hover:text-indigo-600"><i className="fab fa-instagram"></i></a>
                    <a href="#" className="text-gray-600 hover:text-indigo-600"><i className="fab fa-goodreads"></i></a>
                </div>
            </div>
            <div className="border-t border-gray-200 mt-6 pt-6 flex flex-col md:flex-row justify-between">
                <div className="text-sm text-gray-500 mb-4 md:mb-0">
                    &copy; 2023 BookFinder. Tous droits réservés.
                </div>
                <div className="flex space-x-4">
                    <a href="#" className="text-sm text-gray-600 hover:text-indigo-600">Confidentialité</a>
                    <a href="#" className="text-sm text-gray-600 hover:text-indigo-600">Conditions</a>
                    <a href="#" className="text-sm text-gray-600 hover:text-indigo-600">Contact</a>
                </div>
            </div>
        </div>
    </footer>
  );
}
    
