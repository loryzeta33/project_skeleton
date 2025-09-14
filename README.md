# 🗂️ Project Skeleton

**Extract a clean, readable skeleton of any codebase.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-pytest-success.svg)](https://pytest.org)

---

## 📌 Overview

**Project Skeleton** is a modular tool that parses source code projects (e.g. Python) and generates a **readable abstract skeleton** with key structures:

- 📄 Files & directories
- 🏷️ Classes, attributes, methods
- 🧩 Functions, arguments
- 📦 Imports
- 📚 Docstrings (optional)

The output can be exported as **Markdown** or **JSON**.

---

## 🎯 Key Principles

- **Modularity** — Each supported language has its own parser module implementing the same abstract contract.
- **Extensibility** — Adding a new language requires only a new parser module.
- **Separation of Concerns** — Parsing, AST representation, and export are fully decoupled.
- **Output Agnostic** — Export as plain text, Markdown, JSON, or more.

---

## 🚀 Features

✅ Parse Python projects (Java & C support planned).  
✅ Detect classes, functions, imports, docstrings.  
✅ Ignore virtual environments and unwanted folders.  
✅ Output relative paths (optional).  
✅ CLI interface with clear options.  
✅ Easy to extend.  

---

## 📁 Project Structure

```plaintext
project_skeleton/
│
├── src/
│   │
│   ├── skeleton/
│   │   │
│   │   ├── core/
│   │   │   ├── ast_nodes.py      # AST node definitions
│   │   │   ├── parser.py         # ParserBase abstract class
│   │   │   ├── exporter.py       # ExporterBase abstract class
│   │   │
│   │   ├── exporters/
│   │   │   ├── markdown_exporter.py
│   │   │   ├── json_exporter.py
│   │   │
│   │   ├── parsers/
│   │   │   ├── python_parser.py
│   │   │
│   │   ├── cli.py                # CLI entry point (Typer)
│
├── requirements.txt              # Project dependencies
├── tests/                        # Pytest test suite
└── README.md                     # 📄 You are here!
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/loryzeta33/project_skeleton.git
cd project_skeleton
```

### 2. Install in a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e .
```

With the -e option (editable mode), every change to the source code will be instantly reflected in the CLI command.

---

## 🧩 Usage

**Basic usage:**

```bash
skeleton --path <PROJECT_PATH> --language python --output-format markdown
```
**Available CLI options:**

| Option               | Short | Description                                                |
|----------------------|-------|------------------------------------------------------------|
| `--path`             | `-p`  | Path to the project root directory                         |
| `--language`         | `-l`  | Programming language (`python`)                            |
| `--output-format`    | `-o`  | Output format (`markdown` or `json`)                       |
| `--output-file`      | `-f`  | Write output to a file (optional)                          |
| `--exclude-dir`      | `-e`  | Ignore a specific subdirectory (e.g. `.venv`)              |
| `--relative-paths`   | `-r`  | Use relative file paths (default: False)                   |
| `--include-docstring`| `-d`  | Include docstrings in the skeleton (default: False)        |

---

## 🧪 Run Tests

Tests are written with **pytest**.

```bash
# From project root
python -m pytest -v
```

---

## ✏️ Example

```bash
skeleton \
  --path ./my_project \
  --language python \
  --output-format markdown \
  --exclude-dir .venv \
  --relative-paths \
  --include-docstring \
  --output-file skeleton.md
```

---

## 🗂️ Extending the Project

To add support for a new language:

1. Create a new parser module in `parsers/`.
2. Implement `ParserBase` with the `parse()` method.
3. Register the new parser in `cli.py`.

To add a new output format:

1. Create a new exporter in `exporters/`.
2. Implement `ExporterBase` with the `export()` method.

---

## 👥 Contributing

Pull requests and contributions are welcome!
- 📌 Open an issue to propose features or improvements.
- ✅ Please include unit tests with new features.
- 🧹 Follow the same style and naming conventions.

---

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.