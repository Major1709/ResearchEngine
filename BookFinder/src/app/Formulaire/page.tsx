// app/components/Header.tsx
'use client';

import Link from 'next/link';
import { faHome, faAmbulance, faAnchor, faBook} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { useState } from 'react';
import axios from 'axios';

function generateSimpleISBN(): string {
  const part1 = Math.floor(100 + Math.random() * 900); // 3 chiffres
  const part2 = Math.floor(100 + Math.random() * 900); // 3 chiffres
  return `${part1}-${part2}`;
}

export default function Header() {
    const [formData, setFormData] = useState({
    isbn: generateSimpleISBN(),
    title: '',
    author: '',
    year: '',
    grade: '',
    domaine: '',
    directory: null as File | null,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;

    if (type === 'file') {
      const target = e.target as HTMLInputElement;
      const file = target.files?.[0] || null;
      setFormData(prev => ({ ...prev, [name]: file }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log("Formulaire soumis avec :", formData);
    axios.post("http://localhost:8000/uploadfile", formData, {
    headers: { "Content-Type": "multipart/form-data" }
    }).then(response => {
    console.log(response.data);
    });
    
  };
  
  return (
<div className="min-h-screen bg-gray-50">
    <div className="container mx-auto px-4 py-12">
        <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg overflow-hidden">
     
            <div className="gradient-bg p-6 text-white">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-2xl font-bold">
                            <i className="fas fa-book mr-2"></i> Nouveau Livre
                        </h1>
                        <p className="opacity-90 mt-1">Ajoutez un nouveau livre à votre collection</p>
                    </div>
                    <div className="bg-white bg-opacity-20 p-3 rounded-full">
                        <i className="fas fa-book-open text-xl"></i>
                    </div>
                </div>
            </div>

            <form id="bookForm" onSubmit={handleSubmit} className="p-6 space-y-6" encType="multipart/form-data">

                <div>
                    <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                        <i className="fas fa-heading mr-2 text-blue-500"></i>Titre du livre*
                    </label>
                    <input type="text" id="title" name="title" required onChange={handleChange}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200"
                        placeholder="Titre du livre..." />
                </div>


                <div>
                    <label htmlFor="author" className="block text-sm font-medium text-gray-700 mb-1">
                        <i className="fas fa-user-edit mr-2 text-blue-500"></i>Auteur*
                    </label>
                    <input type="text" id="author" name="author" required onChange={handleChange}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200"
                        placeholder="Nom de l'auteur..." />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  
                    <div>
                        <label htmlFor="year" className="block text-sm font-medium text-gray-700 mb-1">
                            <i className="fas fa-calendar-alt mr-2 text-blue-500"></i>Année de publication*
                        </label>
                        <input type="number" id="year" name="year" min="1000" max="2099" required onChange={handleChange}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200"
                            placeholder="Année (ex: 2023)" />
                    </div>

            
                    <div>
                        <label htmlFor="grade" className="block text-sm font-medium text-gray-700 mb-1">
                            <i className="fas fa-star mr-2 text-blue-500"></i>Niveau
                        </label>
                        <div className="relative">
                            <input type="text" id="grade" name="grade" min="1" max="10" required onChange={handleChange}
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200"
                                placeholder="L1, L2, L3, M1, M2, DR, HDR" />
                        </div>
                    </div>
                </div>

                <div>
                    <label htmlFor="domaine" className="block text-sm font-medium text-gray-700 mb-1">
                        <i className="fas fa-tags mr-2 text-blue-500"></i>Domaine*
                    </label>
                    <select id="domaine" name="domaine" required onChange={handleChange}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200">
                        <option value="" disabled>Sélectionnez un domaine</option>
                        <option value="Littérature">Littérature</option>
                        <option value="Science-Fiction">Science-Fiction</option>
                        <option value="Économie">Économie</option>
                        <option value="Philosophie">Philosophie</option>
                        <option value="Informatique">Informatique</option>
                        <option value="Histoire">Histoire</option>
                        <option value="Art">Art</option>
                        <option value="Science">Science</option>
                        <option value="Autre">Autre</option>
                    </select>
                </div>

             
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        <i className="fas fa-folder-open mr-2 text-blue-500"></i>Fichier du livre (PDF, EPUB, etc.)
                    </label>
                    <div className="mt-1 flex items-center">
                        <label htmlFor="directory" className="file-input-label cursor-pointer bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-medium flex items-center">
                            <i className="fas fa-cloud-upload-alt mr-2"></i>
                            <span id="fileLabel">Choisir un fichier</span>
                            <input id="directory" name="directory" type="file" className="hidden" accept=".pdf,.epub,.doc,.docx,.txt" onChange={handleChange} />
                        </label>
                        <span id="fileName" className="ml-4 text-sm text-gray-500 file-name">Aucun fichier sélectionné</span>
                    </div>
                    <p className="mt-1 text-xs text-gray-500">Formats acceptés: PDF, EPUB, DOC, TXT (max 10MB)</p>
                </div>

        
                <div className="pt-4">
                    <button type="submit" 
                        className="w-full gradient-bg hover:opacity-90 text-white font-bold py-3 px-4 rounded-lg transition duration-200 flex justify-center items-center">
                        <i className="fas fa-save mr-2"></i> Enregistrer le livre
                    </button>
                </div>
            </form>
        </div>
    </div>


    <div id="previewModal" className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 hidden">
        <div className="bg-white rounded-xl max-w-md w-full mx-4 max-h-[90vh] overflow-y-auto">
            <div className="gradient-bg p-4 text-white rounded-t-xl flex justify-between items-center">
                <h2 className="text-xl font-bold">
                    <i className="fas fa-eye mr-2"></i> Aperçu du livre
                </h2>
                <button id="closeModal" className="text-white hover:text-gray-200">
                    <i className="fas fa-times"></i>
                </button>
            </div>
            <div className="p-6 space-y-4" id="previewContent">
                {/* Preview content will be inserted here by JavaScript */}
            </div>
            <div className="p-4 border-t flex justify-end space-x-3">
                <button id="cancelBtn" className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition">
                    Annuler
                </button>
                <button id="confirmBtn" className="gradient-bg hover:opacity-90 text-white font-medium py-2 px-6 rounded-lg transition">
                    Confirmer
                </button>
            </div>
        </div>
    </div>
</div>
  );
}