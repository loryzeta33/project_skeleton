# core/ast_nodes.py
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Import:
    module: str
    names: List[str]

@dataclass
class Variable:
    name: str
    type: Optional[str] = None
    default: Optional[str] = None

@dataclass
class Function:
    name: str
    args: List[str]
    docstring: Optional[str] = None

@dataclass
class Class:
    name: str
    attributes: List[Variable] = field(default_factory=list)
    methods: List[Function] = field(default_factory=list)
    docstring: Optional[str] = None

@dataclass
class File:
    path: str
    classes: List[Class] = field(default_factory=list)
    functions: List[Function] = field(default_factory=list)
    imports: List[Import] = field(default_factory=list)

@dataclass
class Project:
    name: str
    files: List[File]
