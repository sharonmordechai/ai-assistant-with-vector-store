"""
This module contains the DocumentLoader class for loading and storing documents of various
formats.

The DocumentLoader supports text, PDF, and Word documents, using loaders defined in the
langchain_community.document_loaders module. It provides methods to load, remove, and get
the size of the documents, and to get the list of supported document extensions.

Also defined are two protocols, FileInitializedClass and FileInitializedDocLoader, for
initializing classes with a file path and BaseLoader classes with a file, respectively.
"""

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

    # The following protocols break pylint for being non-worthy
    # classes (too few methods). We will disable the warning for them.
    # pylint: disable=too-few-public-methods

    class FileInitializedClass(Protocol):
        """A protocol to enforce the initialization of classes with a file path."""

        def __init__(self, file_path: str, *args, **kwargs) -> None: ...

    class FileInitializedDocLoader(BaseLoader, FileInitializedClass):
        """A protocol to enforce BaseLoader classes that initialize with a file."""

    # A dictionary to map file extensions to their respective loaders
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
        """Size of the DocumentLoader is considered the number of documents"""
        return len(self.documents)

    @staticmethod
    def supported_doc_extensions() -> List[str]:
        """Returns the list of supported document extensions"""
        return list(DocumentLoader._DOC_LOADERS.keys())
