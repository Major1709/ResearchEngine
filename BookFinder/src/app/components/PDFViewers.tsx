'use client';

import { Document, Page, pdfjs } from 'react-pdf';
import { useState } from 'react';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';

// Indiquer le chemin du worker
pdfjs.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

export default function PDFViewer({ filePath }: { filePath: string }) {
  const [, setNumPages] = useState<number | null>(null);

  const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
    setNumPages(numPages);
  };

  return (
    <div className="w-full h-auto">
      <Document file={filePath} onLoadSuccess={onDocumentLoadSuccess}          
            loading={<div>Chargement PDF...</div>}
          error={<div>Impossible de charger le PDF</div>}>
        <Page pageNumber={1} width={300} />
      </Document>
    </div>
  );
}
