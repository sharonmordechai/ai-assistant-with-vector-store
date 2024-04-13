import os

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.word_document import Docx2txtLoader


class DocumentLoader:
    """
    A class to load documents of various formats and store them in a list.

    Attributes:
        documents (list): A list to store the loaded documents.

    Example usage:
        loader = DocumentLoader()
        loader.load("<path/to/file>")
        print(loader.size())
        loader.remove("<path/to/file>")
        print(loader.size())
    """

    def __init__(self):
        """
        Initializes an empty list to store the documents.
        """
        self.documents = []

    def load(self, file_path):
        """
        Loads a document from the specified file path and appends it to the documents list.

        Args:
            file_path (str): The path to the document file to be loaded.
        """
        file_type = self.get_file_type(file_path)

        if file_type == "txt":
            # Text loader for txt files
            loader = TextLoader(file_path)
            self.documents.extend(loader.load())
        elif file_type == "pdf":
            # PDF loader for pdf files
            loader = PyPDFLoader(file_path)
            self.documents.extend(loader.load())
        elif file_type == "docx":
            # Word loader for docx files
            loader = Docx2txtLoader(file_path)
            self.documents.extend(loader.load())
        else:
            print(f"{file_type} is not supported.")
            return

    def remove(self, file_path):
        """
        Removes a document from the documents list based on its source path.

        Args:
            file_path (str): The path of the document to be removed.
        """
        filename = os.path.basename(file_path)
        for doc in self.documents:
            doc_filename = os.path.basename(doc.metadata.get("source"))
            if doc_filename == filename:
                self.documents.remove(doc)
                break

    def size(self):
        return len(self.documents)

    @staticmethod
    def get_file_type(file_path):
        """
        Determines the file type based on the file extension.

        Args:
            file_path (str): The path to the file.

        Returns:
            str: The file type (txt, pdf, docx).
        """
        _, ext = os.path.splitext(file_path)
        return ext[1:].lower()
