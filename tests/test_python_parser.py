# tests/test_python_parser.py

import textwrap
from skeleton.parsers.python_parser import PythonParser


def test_parse_simple_python_file(tmp_path):
    """
    Verify that the PythonParser extracts classes, functions and imports from a simple file.
    """

    code = textwrap.dedent("""
        import os
        from sys import argv

        class MyClass:
            def method1(self):
                pass

        def function1():
            pass

        def function2():
            pass
    """)

    test_file = tmp_path / "sample.py"
    test_file.write_text(code, encoding="utf-8")

    parser = PythonParser()
    project = parser.parse(tmp_path)

    assert len(project.files) == 1

    file = project.files[0]
    assert len(file.imports) == 2
    assert len(file.classes) == 1
    assert len(file.functions) == 3

    top_level_funcs = [f for f in file.functions if "function" in f.name]
    assert len(top_level_funcs) == 2

    cls = file.classes[0]
    assert cls.name == "MyClass"
    assert len(cls.methods) == 1
    assert cls.methods[0].name == "method1"

    func1 = file.functions[0]
    assert func1.name == "function1"
    func2 = file.functions[1]
    assert func2.name == "function2"
