# cli.py

import typer
from pathlib import Path

from skeleton.parsers.python_parser import PythonParser
from skeleton.exporters.markdown_exporter import MarkdownExporter
from skeleton.exporters.json_exporter import JSONExporter

app = typer.Typer(help="🗂️ Generate a readable skeleton of your project.")

@app.command()
def generate(
    path: str = typer.Option(..., "--path", "-p", help="Path to the project or file."),
    language: str = typer.Option("python", "--language", "-l", help="Programming language."),
    output_format: str = typer.Option("markdown", "--output-format", "-o", help="Output format."),
    output_file: str = typer.Option(None, "--output-file", "-f", help="Output path (optional)."),
    exclude_dir: list[str] = typer.Option(None, "--exclude-dir", "-e", help="Extra folders to exclude (es: build dist)"),
    relative_paths: bool = typer.Option(False, "--relative-paths", "-r", help="Use relative file paths."),
    include_docstrings: bool = typer.Option(False, "--include-docstrings", "-d", help="Include docstring of classes and functions.")
):
    """
    Analyze the project and generate the skeleton in thr chosen format.
    """
    # Parser selection
    if language == "python":
        parser = PythonParser(
            extra_ignore=exclude_dir,
            use_relative_paths=relative_paths,
            include_docstrings=include_docstrings
        )
    else:
        typer.echo(f"❌ Parser for '{language}' not available.")
        raise typer.Exit(code=1)

    project = parser.parse(path)

    # Exporter selection
    if output_format == "markdown":
        exporter = MarkdownExporter()
    elif output_format == "json":
        exporter = JSONExporter()
    else:
        typer.echo(f"❌ Exporter for '{output_format}' not available.")
        raise typer.Exit(code=1)

    result = exporter.export(project)

    if output_file:
        output_path = Path(output_file)
        output_path.write_text(result, encoding="utf-8")
        typer.echo(f"✅ Skeleton generated in '{output_file}'")
    else:
        print(result)


if __name__ == "__main__":
    app()
