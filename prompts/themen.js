// Ein Item pro Thema; der HTTP Request läuft dann einmal pro Item
const themen = [
  { thema: 'AI allgemein', max: 40,
    query: 'cat:cs.AI' },
  { thema: 'AI in Society', max: 30,
    query: '(cat:cs.CY OR cat:cs.HC) AND (abs:AI OR abs:"machine learning" OR abs:"language model")' },
  { thema: 'AI in Medicine', max: 30,
    query: '(cat:cs.AI OR cat:cs.LG OR cat:cs.CV OR cat:eess.IV) AND (abs:clinical OR abs:medical OR abs:patient OR abs:healthcare)' },
  { thema: 'Computational Neuroscience', max: 30,
    query: 'cat:q-bio.NC' },
  { thema: 'Neurotech & BCI', max: 20,
    query: 'abs:"brain-computer interface" OR abs:"brain-machine interface" OR abs:neurotechnology OR abs:"neural interface" OR (cat:eess.SP AND abs:EEG)' },
];

// Nur Papers der letzten 7 Tage (arXiv-Format JJJJMMTTHHMM, GMT)
const fmt = d => d.toISOString().slice(0, 16).replace(/[-T:]/g, '');
const bis = new Date();
const von = new Date(bis.getTime() - 7 * 24 * 60 * 60 * 1000);
const zeitraum = ` AND submittedDate:[${fmt(von)} TO ${fmt(bis)}]`;

return themen.map(t => ({ json: { ...t, query: `(${t.query})${zeitraum}` } }));
