import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const { name } = req.query;

  if (typeof name !== 'string') {
    res.status(400).send('Nom de fichier invalide');
    return;
  }

  // 🔁 Chemin absolu vers ton dossier PDF
  const filePath = path.resolve('/home/toma/Documents/monprojet/pdfs', name);

  if (!fs.existsSync(filePath)) {
    res.status(404).send('Fichier introuvable');
    return;
  }

  const fileStream = fs.createReadStream(filePath);
  res.setHeader('Content-Type', 'application/pdf');
  fileStream.pipe(res);
}
