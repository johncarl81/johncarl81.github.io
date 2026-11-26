"""Builds SVG publication figures from the LaTeX sources cloned into ~/dev/paper-sources.

Each figure is wrapped in a standalone document with the same \\includegraphics options
the paper uses, compiled with pdflatex, converted with pdftocairo, and any embedded
bitmaps are re-encoded as WebP to keep the SVGs small.

Usage: python3 scripts/build_publication_figures.py [figure-name ...]
"""
import base64
import pathlib
import re
import subprocess
import sys
import tempfile

SOURCES = pathlib.Path.home() / "dev" / "paper-sources"
BUILD = pathlib.Path(tempfile.gettempdir()) / "publication-figures"
OUTPUT = pathlib.Path(__file__).resolve().parent.parent / "images" / "publications"
WEBP_QUALITY = "80"
MAX_EMBEDDED_SIZE = "1200x1200>"

PREAMBLE = r"""\documentclass[border=2pt]{standalone}
\usepackage{mathptmx}
\usepackage{graphicx}
\usepackage{tikz}
\begin{document}
"""

FIGURES = {
    "ssrr-2024-fig3": r"""\begin{tikzpicture}[scale=0.7]
    \node at (0,0) {\includegraphics[scale = 0.56, trim={2.7cm 4cm 24cm 2.75cm}, clip]{%(dir)s/sketch-implementation-ssrr-2024/figures/sketch_dynamics.pdf}};
    \node at (1.3,-0.35) {$\alpha$};
    \node at (2.6,-0.25) {$c$};
    \node at (-2.6, 0.35) {$\lambda$};
    \node at (0.2, -3.25) {$\lambda$};
    \node at (-1.2,-4.3) {$\sqrt{\lambda}$};
    \node[circle, draw, inner sep=1pt] at (0.5,-4.3) {1};
    \node[circle, draw, inner sep=1pt] at (0.5,-0.9) {2};
    \node[circle, draw, inner sep=1pt] at (1.5,1) {3};
\end{tikzpicture}""",
    "amt-2024-fig2": r"""\includegraphics[trim={8cm 1cm 3cm 1cm}, clip]{%(dir)s/ericksen-amt2023/Figures/lat_lon_krig.pdf}""",
    "frontiers-2022-fig4": r"""\includegraphics[trim={0cm 10.5cm 22cm 0cm}, clip]{%(dir)s/volcan-iros2021/figures/Dragonfly_Flocking_Detail.pdf}""",
}


def recompress_embedded_images(svg):
    """Re-encodes embedded PNG bitmaps as WebP when that makes them smaller."""
    def replace(match):
        png = base64.b64decode(match.group(1))
        source = BUILD / "embedded.png"
        target = BUILD / "embedded.webp"
        source.write_bytes(png)
        subprocess.run(["convert", str(source), "-resize", MAX_EMBEDDED_SIZE, "-quality", WEBP_QUALITY, str(target)], check=True)
        webp = target.read_bytes()
        if len(webp) < len(png):
            return "data:image/webp;base64," + base64.b64encode(webp).decode()
        return match.group(0)

    return re.sub(r"data:image/png;base64,([A-Za-z0-9+/=\s]+)", replace, svg)


def build(name, body):
    tex = BUILD / f"{name}.tex"
    tex.write_text(PREAMBLE + body % {"dir": SOURCES} + "\n\\end{document}\n")
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex.name],
                   cwd=BUILD, check=True, stdout=subprocess.DEVNULL)
    raw_svg = BUILD / f"{name}.svg"
    subprocess.run(["pdftocairo", "-svg", str(BUILD / f"{name}.pdf"), str(raw_svg)], check=True)
    svg = recompress_embedded_images(raw_svg.read_text())
    (OUTPUT / f"{name}.svg").write_text(svg)
    return raw_svg.stat().st_size, len(svg.encode())


if __name__ == "__main__":
    BUILD.mkdir(parents=True, exist_ok=True)
    for figure_name in sys.argv[1:] or FIGURES:
        raw_size, final_size = build(figure_name, FIGURES[figure_name])
        print(f"{figure_name}: {raw_size // 1024} KB raw -> {final_size // 1024} KB")
