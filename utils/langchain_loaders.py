# built-ins
from pathlib import Path
from typing import Dict, List, Protocol, Type

# 3rd-party
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.word_document import Docx2txtLoader
from langchain_core.documents import Document


class DocumentLoader:
    """
    A class to load documents of various formats and store them in a list.

    Attributes:
        documents: A list to store the loaded documents.

    Example usage:
        loader = DocumentLoader()
        loader.load("<path/to/file>")
        print(loader.size())
        loader.remove("<path/to/file>")
        print(loader.size())
    """

    # A protocol to enforce the initialization of classes with a file path
    class FileInitializedClass(Protocol):
        def __init__(self, file_path: str, *args, **kwargs) -> None: ...

    # A protocol to enforce BaseLoader classes that initialize with a file
    class FileInitializedDocLoader(BaseLoader, FileInitializedClass):
        pass

    # A dictionary to map file extensions to their respective loaders
    # Sadly,
    _DOC_LOADERS: Dict[str, Type[FileInitializedDocLoader]] = {
        "txt": TextLoader,
        "pdf": PyPDFLoader,
        "docx": Docx2txtLoader,
    }

    def __init__(self) -> None:
        """
        Initializes an empty list to store the documents.
        """
        self.documents: List[Document] = []

    def load(self, doc_path: Path) -> None:
        """
        Loads a document from the specified file path and appends it to the documents list.

        Args:
            doc_path: The path to the document file to be loaded.
        """
        file_ext = doc_path.suffix[1:]
        try:
            loader: BaseLoader = DocumentLoader._DOC_LOADERS[file_ext](str(doc_path))
            self.documents.extend(loader.load())
        except KeyError:
            print(f"{file_ext} is not supported.")
            return

    def remove(self, doc_path: Path) -> None:
        """
        Removes a document from the documents list based on its source path.

        Args:
            doc_path: The path of the document to be removed.
        """
        doc_filename_to_remove = doc_path.stem
        for doc in self.documents:
            doc_filename = Path(doc.metadata.get("source")).stem
            if doc_filename == doc_filename_to_remove:
                self.documents.remove(doc)
                break

    @property
    def size(self) -> int:
        return len(self.documents)

    @staticmethod
    def supported_doc_extensions() -> List[str]:
        return list(DocumentLoader._DOC_LOADERS.keys())
