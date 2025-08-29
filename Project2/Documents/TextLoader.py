
from datetime import datetime
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

class TextLoader:
    def __init__(self, filepath, encoding="utf-8"):
        self.filepath = filepath
        self.encoding = encoding

    def load(self):
        with open(self.filepath, "r", encoding=self.encoding) as f:
            content = f.read()

        metadata = {
            "source": self.filepath,
            "length": len(content),
            "loaded_at": datetime.now().isoformat()
        }

        return [Document(page_content=content, metadata=metadata)]
