# exporters/json_exporter.py

import json
from skeleton.core.exporter import ExporterBase
from skeleton.core.ast_nodes import Project


class JSONExporter(ExporterBase):
    """
    Export the project skeleton in JSON format.
    """

    def export(self, project: Project) -> str:
        # Transform the AST into a recursive dictionary.
        def file_to_dict(file):
            return {
                "path": file.path,
                "imports": [
                    {"module": imp.module, "names": imp.names} for imp in file.imports
                ],
                "classes": [
                    {
                        "name": cls.name,
                        "docstring": cls.docstring,
                        "attributes": [
                            {
                                "name": var.name,
                                "type": var.type,
                                "default": var.default
                            } for var in cls.attributes
                        ],
                        "methods": [
                            {
                                "name": m.name,
                                "args": m.args,
                                "docstring": m.docstring
                            } for m in cls.methods
                        ]
                    } for cls in file.classes
                ],
                "functions": [
                    {
                        "name": func.name,
                        "args": func.args,
                        "docstring": func.docstring
                    } for func in file.functions
                ]
            }

        project_dict = {
            "name": project.name,
            "files": [file_to_dict(f) for f in project.files]
        }

        return json.dumps(project_dict, indent=4)
