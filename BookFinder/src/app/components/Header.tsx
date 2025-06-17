'use client';

import Link from 'next/link';
import { faHome, faAmbulance, faAnchor, faBook, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { useRouter } from 'next/navigation'; // ✅ CORRECTION ICI

export default function Header() {
  const router = useRouter();

  const handleNavigate = () => {
    router.push('/Formulaire');
  };

  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto px-4 py-6 flex justify-between items-center">
        <div className="flex items-center">
          <FontAwesomeIcon icon={faBook} className="open text-3xl text-indigo-600 mr-3 floating" />
          <h1 className="text-2xl font-bold text-gray-800">BookFinder</h1>
        </div>
        <div className="flex items-center space-x-4">
          <Link href="/"><FontAwesomeIcon icon={faHome} className="text-gray-600 hover:text-indigo-600" /></Link>
          <Link href="#"><FontAwesomeIcon icon={faAmbulance} className="text-gray-600 hover:text-indigo-600" /></Link>
          <button onClick={handleNavigate}>
            <FontAwesomeIcon icon={faPlus} className="text-gray-600 hover:text-indigo-600" />
          </button>
        </div>
      </div>
    </header>
  );
}
