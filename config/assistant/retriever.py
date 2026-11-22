"""Knowledge-base retrieval: chunk articles, index with TF-IDF, return top-k chunks.

TF-IDF (not embeddings) keeps the lab dependency-light and deterministic. The
failure modes it demonstrates (stale documents, bad chunking, low-confidence
retrieval) are the same ones that show up with embedding-based RAG.
"""
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def parse_doc(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    meta: dict = {}
    body = text
    if text.startswith("---"):
        _, front, body = text.split("---", 2)
        for line in front.strip().splitlines():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta, body.strip()


def chunk_words(text: str, size: int, overlap: int) -> list[str]:
    words = text.split()
    step = max(size - overlap, 1)
    chunks = []
    for start in range(0, len(words), step):
        piece = words[start:start + size]
        if piece:
            chunks.append(" ".join(piece))
        if start + size >= len(words):
            break
    return chunks


class Retriever:
    def __init__(self, kb_dirs: list[str], chunk_size: int, overlap: int, root: Path):
        self.chunks: list[dict] = []
        for kb_dir in kb_dirs:
            for path in sorted((root / kb_dir).glob("*.md")):
                meta, body = parse_doc(path)
                for idx, text in enumerate(chunk_words(body, chunk_size, overlap)):
                    self.chunks.append({
                        "doc_id": path.stem,
                        "title": meta.get("title", path.stem),
                        "topic": meta.get("topic", ""),
                        "updated": meta.get("updated", ""),
                        "chunk_idx": idx,
                        "text": text,
                        "words": len(text.split()),
                    })
        # Index the article title together with each chunk so a chunk keeps its topic
        # context. The answer still quotes only the chunk text.
        self.vectorizer = TfidfVectorizer(stop_words="english", sublinear_tf=True)
        self.matrix = self.vectorizer.fit_transform([f"{c['title']} {c['text']}" for c in self.chunks])

    def search(self, query: str, k: int) -> list[dict]:
        scores = cosine_similarity(self.vectorizer.transform([query]), self.matrix)[0]
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [{**self.chunks[i], "score": round(float(scores[i]), 3)} for i in ranked]
