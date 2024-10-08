"""Generate the code reference pages and navigation."""

from pathlib import Path

import mkdocs_gen_files

EXCLUDE = [
    "ldctbench/scripts/download_data.py",
    "ldctbench/scripts/train.py",
    "ldctbench/scripts/test.py",
]

nav = mkdocs_gen_files.Nav()

for path in sorted(Path("ldctbench").rglob("*.py")):
    if path.name[0] == "_":
        continue
    if str(path) in EXCLUDE:
        continue

    module_path = path.relative_to(".").with_suffix("")
    doc_path = path.relative_to(".").with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"#{ident}\n")
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)
