# exporters/markdown_exporter.py

from skeleton.core.exporter import ExporterBase
from skeleton.core.ast_nodes import Project


class MarkdownExporter(ExporterBase):
    """
    Export the project skeleton in a legible Markdown format.
    """

    def export(self, project: Project) -> str:
        lines = [f"# 📁 {project.name}\n"]

        for file in project.files:
            lines.append(f"## File: `{file.path}`\n")

            if file.imports:
                lines.append("**Imports:**")
                for imp in file.imports:
                    names = ', '.join(imp.names) if imp.names else '*'
                    lines.append(f"- `{imp.module}` ({names})")

            if file.classes:
                lines.append("\n**Classes:**")
                for cls in file.classes:
                    lines.append(f"- `{cls.name}`")
                    if cls.docstring:
                        lines.append(f"  - Docstring:")
                        lines.extend(self._format_docstring(cls.docstring, indent="    "))
                    if cls.attributes:
                        lines.append("  - Attributes:")
                        for attr in cls.attributes:
                            attr_type = f": {attr.type}" if attr.type else ""
                            default = f" = {attr.default}" if attr.default else ""
                            lines.append(f"    - `{attr.name}`{attr_type}{default}")
                    if cls.methods:
                        lines.append("  - Methods:")
                        for m in cls.methods:
                            args = ', '.join(m.args)
                            lines.append(f"    - `{m.name}({args})`")
                            if m.docstring:
                                lines.append(f"      - Docstring:")
                                lines.extend(self._format_docstring(m.docstring, indent="        "))

            if file.functions:
                lines.append("\n**Functions:**")
                for func in file.functions:
                    args = ', '.join(func.args)
                    lines.append(f"- `{func.name}({args})`")
                    if func.docstring:
                        lines.append(f"  - Docstring:")
                        lines.extend(self._format_docstring(func.docstring, indent="    "))

            lines.append("\n---\n")

        return '\n'.join(lines)

    def _format_docstring(self, docstring: str, indent: str = "  ") -> list[str]:
        """
        Format a docstring as indented lines.
        """
        lines = docstring.strip().splitlines()
        result = []
        for line in lines:
            if line.strip() == "":
                result.append("")
            else:
                result.append(f"{indent}{line}")
        return result