from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
@dataclass
class Document:
    """
    A universal data structure for all document types.
    Works with loaders, chunkers, embeddings, and LLMs.
    """
    page_content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    blob: Optional[bytes] = None       # raw binary (for images)
    resources: Optional[List[str]] = field(default_factory=list)  # extracted file paths, images, etc.
    id: Optional[str] = None
    
    def __repr__(self):
        preview = self.page_content[:80].replace("\n", " ") + ("..." if len(self.page_content) > 80 else "")
        return f"<Document id={self.id} source={self.metadata.get('source','')} content='{preview}'>"


class RecursiveCharacterTextSplitter:
    def __init__(self, chunk_size=500, chunk_overlap=50, separators=None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", " ", ""]

    def split_text(self, text: str):
        for sep in self.separators:
            if sep and sep in text:
                parts = text.split(sep)
                break
        else:
            parts = list(text)

        chunks, current_chunk = [], ""
        for part in parts:
            piece = part + (sep if sep else "")
            if len(current_chunk + piece) > self.chunk_size:
                if current_chunk:
                    chunks.extend(self._split_chunk(current_chunk))
                current_chunk = piece
            else:
                current_chunk += piece

        if current_chunk:
            chunks.extend(self._split_chunk(current_chunk))
        return chunks

    def _split_chunk(self, text: str):
        chunks, start = [], 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += self.chunk_size - self.chunk_overlap
        return chunks

    def split_documents(self, documents: list):
        chunked_docs = []
        for doc in documents:
            chunks = self.split_text(doc.page_content)
            for i, chunk in enumerate(chunks):
                metadata = dict(doc.metadata) if doc.metadata else {}
                metadata["chunk"] = i
                chunked_docs.append(Document(page_content=chunk, metadata=metadata))
        return chunked_docs
