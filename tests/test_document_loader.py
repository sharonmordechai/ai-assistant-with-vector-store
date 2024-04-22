"""
This module contains tests for the DocumentLoader class, which is responsible for
loading and storing documents of various formats.

The DocumentLoader supports text, PDF, and Word documents, utilizing loaders defined
in the utils.langchain_loaders module.
It provides methods to load, remove, and get the size of the documents, as well as to
get the list of supported document extensions.
"""

# built-ins
from pathlib import Path

# 3rd-party
import pytest
from langchain_community.document_loaders.text import TextLoader

# local
from utils.langchain_loaders import DocumentLoader

# Define the path to the test files
TEST_FILES_PATH = Path(__file__).parent / "files"


# pylint: disable=redefined-outer-name
@pytest.fixture
def document_loader() -> DocumentLoader:
    """Fixture to create a new DocumentLoader instance."""
    return DocumentLoader()


def _test_load_file(loader, file_name: str, expected_loader) -> None:
    """Helper function to test loading a file."""
    file_path = TEST_FILES_PATH / file_name
    loader.load(file_path)
    assert loader.size == 1, f"Expected size to be 1, but got {loader.size}"
    assert (
        loader.documents[0].page_content
        == expected_loader(file_path).load()[0].page_content
    ), "Loaded document content does not match expected content"


def test_load_txt_file(document_loader: DocumentLoader) -> None:
    """Test loading a txt file."""
    _test_load_file(document_loader, "test_file.txt", TextLoader)


def test_remove_file(document_loader: DocumentLoader) -> None:
    """Test removing a file."""
    file_path = TEST_FILES_PATH / "test_file.txt"
    document_loader.load(file_path)
    assert document_loader.size == 1, "Expected size to be 1 after loading the file"
    document_loader.remove(file_path)
    assert document_loader.size == 0, "Expected size to be 0 after removing the file"


def test_supported_doc_extensions() -> None:
    """Test supported document extensions."""
    expected_extensions = {"txt", "pdf", "docx"}
    assert (
        set(DocumentLoader.supported_doc_extensions()) == expected_extensions
    ), f"Expected extensions: {expected_extensions}"


def test_load_unsupported_file_type(document_loader: DocumentLoader) -> None:
    """Test loading an unsupported file type."""
    file_path = TEST_FILES_PATH / "test_file.csv"
    assert document_loader.load(file_path) is False, "Expected load to return False"
