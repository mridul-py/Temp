# Utils/Document.py
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
    def __init__():
        pass
    def __repr__(self):
        preview = self.page_content[:80].replace("\n", " ") + ("..." if len(self.page_content) > 80 else "")
        return f"<Document id={self.id} source={self.metadata.get('source','')} content='{preview}'>"
