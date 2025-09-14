# core/exporter.py

from abc import ABC, abstractmethod
from .ast_nodes import Project


class ExporterBase(ABC):
    """
    Base interface for all exporters.
    """

    @abstractmethod
    def export(self, project: Project) -> str:
        """
        Receives a Project and returns a string representation the skeleton in the desire format.

        Args:
            project: Project instance

        Returns:
            The string representation
        """
        pass
