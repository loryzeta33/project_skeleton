# core/parser.py

from abc import ABC, abstractmethod
from .ast_nodes import Project


class ParserBase(ABC):
    """
    Base interface for languages' parsers.
    """

    @abstractmethod
    def parse(self, path: str) -> Project:
        """
        Parse a file or a source code folder.

        Args:
            path (str): Path to the file or a source code folder

        Returns:
            a Project object
        """
        pass
