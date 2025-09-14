# parsers/python_parser.py

import ast
import os
from pathlib import Path
from typing import List, Optional

from skeleton.core.parser import ParserBase
from skeleton.core.ast_nodes import Project, File, Class, Function, Variable, Import


class PythonParser(ParserBase):
    """
    Parser for Python projects.
    Use the standard library `ast` module.
    """
    DEFAULT_IGNORE_DIRS = ['.venv', 'venv', '.env', 'env']

    def __init__(self, extra_ignore: Optional[List[str]] = None, use_relative_paths: bool = False, include_docstrings: bool = False):
        self.ignore_dirs = set(self.DEFAULT_IGNORE_DIRS)
        if extra_ignore:
            self.ignore_dirs.update(extra_ignore)
        self.use_relative_paths = use_relative_paths
        self.include_docstrings = include_docstrings

    def parse(self, path: str) -> Project:
        """
        Parse all .py files in `path` (also recursively) and build the AST Project.
        """
        project_path = Path(path)
        if not project_path.exists():
            raise FileNotFoundError(f"{path} doesn't exists.")

        project_name = project_path.stem

        ignored_found = set()
        files = []

        for root, dirs, filenames in os.walk(project_path):
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]

            for name in dirs:
                if name in self.ignore_dirs:
                    ignored_found.add(name)

            for filename in filenames:
                if filename.endswith(".py"):
                    file_path = Path(root) / filename
                    if self.use_relative_paths:
                        file_path_str = str(file_path.relative_to(project_path))
                    else:
                        file_path_str = str(file_path.resolve())
                    files.append(self._parse_file(file_path, file_path_str))

        if ignored_found:
            print(f"🔍 Ignored virtual environment directories: {', '.join(sorted(ignored_found))}")

        return Project(name=project_name, files=files)

    def _parse_file(self, path: Path, path_str: str) -> File:
        """
        Parsa a single .py file.
        """
        with path.open(encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)
        classes, functions, imports = [], [], []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(self._parse_class(node))
            elif isinstance(node, ast.FunctionDef):
                functions.append(self._parse_function(node))
            elif isinstance(node, ast.Import):
                imports.extend(self._parse_import(node))
            elif isinstance(node, ast.ImportFrom):
                imports.extend(self._parse_importfrom(node))

        return File(path=path_str, classes=classes, functions=functions, imports=imports)

    def _parse_class(self, node: ast.ClassDef) -> Class:
        """
        Extract info from a class definition.
        """
        methods: List[Function] = []
        attributes: List[Variable] = []

        for body_item in node.body:
            if isinstance(body_item, ast.FunctionDef):
                methods.append(self._parse_function(body_item))
            elif isinstance(body_item, ast.Assign):
                # Esempio: class-level attribute
                for target in body_item.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        attributes.append(Variable(name=var_name))

        docstring = ast.get_docstring(node) if self.include_docstrings else None

        return Class(
            name=node.name,
            methods=methods,
            attributes=attributes,
            docstring=docstring
        )

    def _parse_function(self, node: ast.FunctionDef) -> Function:
        """
        Extract info from a function or a method definition.
        """
        args = [arg.arg for arg in node.args.args]
        docstring = ast.get_docstring(node)
        return Function(
            name=node.name,
            args=args,
            docstring=docstring
        )

    def _parse_import(self, node: ast.Import) -> List[Import]:
        """
        Extract modules from an import statement.
        """
        result = []
        for alias in node.names:
            result.append(Import(module=alias.name, names=["*"]))
        return result

    def _parse_importfrom(self, node: ast.ImportFrom) -> List[Import]:
        """
        Extract modules from an import 'from X import a, b'.
        """
        names = [alias.name for alias in node.names]
        return [Import(module=node.module or "", names=names)]
