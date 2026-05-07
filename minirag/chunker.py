from pathlib import Path
from pypdf import PdfReader
from bs4 import BeautifulSoup

from typing import List, Dict, Optional

from config import CHUNK_SIZE, CHUNK_OVERLAP, ALLOWED_EXTS


def _load_pdf(path):
    reader = PdfReader(path)
    docs = []
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        text = text.strip()
        if not text:
            continue
        docs.append({
            "text": text,
            "metadata": {
                "source": str(Path(path).name),
                "type": "pdf",
                "page": page_num,
            }
        })
    return docs

def _load_html(path):
    html = Path(path).read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    main_text = soup.get_text("\n", strip=True)
    title = soup.title.string.strip() if soup.title and soup.title.string else None

    return [{
        "text": main_text,
        "metadata": {
            "source": str(Path(path).name),
            "type": "html",
            "title": title,
        }
    }]


def load_documents(file_paths: List[Path]) -> List[Dict]:
    # docs_path = Path(docs_path)
    #
    # if not docs_path.exists() or not docs_path.is_dir():
    #     raise NotADirectoryError(f"Folder not found or is not a directory: {docs_path}")
    #
    # file_paths = [
    #     p for p in docs_path.rglob("*")
    #     if p.is_file()
    #     and p.suffix.lower() in ALLOWED_EXTS
    #     and not any(i.startswith('.') for i in p.parts)
    # ]

    all_docs = []
    for path in file_paths:
        ext = path.suffix.lower()
        if ext == ".pdf":
            all_docs.extend(_load_pdf(path))
        elif ext in {".html", ".htm"}:
            all_docs.extend(_load_html(path))
        else:
            # Plain text fallback for any other file type
            text = path.read_text(encoding="utf-8")
            all_docs.append({
                "text": text,
                "metadata": {
                    "source": path.name,
                    "type": "text",
                }
            })

    return all_docs

def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP
) -> List[str]:
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += chunk_size - chunk_overlap

    return chunks

def chunk_documents(
        docs: List[Dict],
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP
) -> List[Dict]:
    chunked_docs = []
    count = 0

    for doc in docs:
        base_text = doc["text"]
        base_meta = doc["metadata"]

        for i, chunk in enumerate(chunk_text(base_text, chunk_size, chunk_overlap)):
            if not chunk:
                continue
            chunked_docs.append({
                "id": count,
                "text": chunk,
                "metadata": {
                    **base_meta,
                    "chunk_index": i,
                }
            })
            count += 1

    return chunked_docs

if __name__ == "__main__":
    pass