# tests/test_exporter.py

from skeleton.core.ast_nodes import Project, File, Class, Function, Variable, Import
from skeleton.exporters.markdown_exporter import MarkdownExporter
from skeleton.exporters.json_exporter import JSONExporter
import json


def test_markdown_exporter_output():
    """
    Verify that the MarkdownExporter produce a legible output.
    """
    project = Project(
        name="Project Skeleton",
        files=[
            File(
                path="test.py",
                imports=[Import(module="os", names=["*"])],
                classes=[
                    Class(
                        name="MyClass",
                        attributes=[Variable(name="attr")],
                        methods=[Function(name="method", args=["self"])]
                    )
                ],
                functions=[Function(name="my_function", args=[])]
            )
        ]
    )

    exporter = MarkdownExporter()
    output = exporter.export(project)

    assert "# 📁 Project Skeleton" in output
    assert "## File: `test.py`" in output
    assert "- `os` (*)" in output or "- `os`" in output
    assert "- `MyClass`" in output
    assert "method(self)" in output
    assert "my_function()" in output


def test_json_exporter_output():
    """
    Verify that the JSONExporter produce a coherent JSON output.
    """
    project = Project(
        name="test_project",
        files=[
            File(
                path="test.py",
                imports=[Import(module="os", names=["*"])],
                classes=[
                    Class(
                        name="MyClass",
                        attributes=[Variable(name="attr", type="int", default="0")],
                        methods=[Function(name="method", args=["self"], docstring="Example method")]
                    )
                ],
                functions=[Function(name="my_function", args=["x"], docstring="Example func")]
            )
        ]
    )

    exporter = JSONExporter()
    output = exporter.export(project)
    data = json.loads(output)

    assert "files" in data
    assert data["files"][0]["path"] == "test.py"
    assert data["files"][0]["imports"][0]["module"] == "os"
    assert data["files"][0]["classes"][0]["name"] == "MyClass"
    assert data["files"][0]["classes"][0]["attributes"][0]["name"] == "attr"
    assert data["files"][0]["functions"][0]["name"] == "my_function"
