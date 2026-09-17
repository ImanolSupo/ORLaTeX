# Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c.
# See NOTICE.md and MANIFEST.txt for work scope and maintenance.

"""Smoke-test independent and duplicate loaders in isolated installations."""
from pathlib import Path
import tempfile
from compile import ROOT, ENGINES, compile_source


def main():
    staging = ROOT / "tmp/alias-smoke"
    staging.mkdir(parents=True, exist_ok=True)
    source = (ROOT / "examples/00-quickstart.tex").read_text(encoding="utf-8")
    loaders = ("orlatex", "ortex", "ormath", "orlatex,ortex,ormath,orlatex", "ormath,ortex,orlatex,ormath")
    with tempfile.TemporaryDirectory(prefix="install-", dir=staging) as directory:
        install = Path(directory)
        for name in ("orlatex.sty", "orlatex-input.code.tex", "ortex.sty", "ormath.sty"):
            (install / name).write_bytes((ROOT / name).read_bytes())
        for index, loader in enumerate(loaders, 1):
            example = install / f"alias-{index:02d}.tex"
            example.write_text(source.replace("\\usepackage{orlatex}", "\\usepackage{" + loader + "}"), encoding="utf-8")
            for engine in ENGINES:
                compile_source(example, engine, ROOT / "output/alias-smoke" / engine, cwd=install)
    print("PASS five loader combinations on three engines, two passes each")


if __name__ == "__main__":
    main()
