"""Generate the profile banner.

Pure SMIL. GitHub serves the file through its image proxy, where CSS and JS do
not run, so every animation here is a native SVG one. Nothing is revealed by
animation — each element is drawn at its resting appearance and motion sits on
top, so the banner still reads correctly if nothing moves.

The figure is a causal attention matrix, computed rather than decorated: row i
can only attend to positions 0..i, there is a sink at position 0, a strong
diagonal, and a decaying local window. A query position sweeps down the rows
and lights that row's real weights. It is the picture a transformer produces.
"""

from __future__ import annotations

import math
import pathlib

W, H = 1200, 340
N = 16                      # sequence positions shown
CELL, GAP = 11.5, 2.0
GRID = N * (CELL + GAP) - GAP
GX = W - GRID - 118         # grid left edge
GY = (H - GRID) / 2 + 4     # grid top edge, nudged for the caption

THEMES = {
    "dark": dict(
        bg="#080b0f", panel="#0d1219", rule="#1b2430",
        ink="#f2f5f8", dim="#8a97a5", faint="#4d5866",
        accent="#22d3c5", warm="#f2b544",
    ),
    "light": dict(
        bg="#fbfcfd", panel="#f1f5f9", rule="#dde4ec",
        ink="#0a0f16", dim="#5a6673", faint="#98a4b2",
        accent="#0d9488", warm="#b0741a",
    ),
}


def attention() -> list[list[float]]:
    """A causal attention pattern, row-normalised.

    Three components that show up in real trained models: an attention sink at
    position 0, self-attention on the diagonal, and an exponentially decaying
    window over recent positions.
    """
    rows: list[list[float]] = []
    for i in range(N):
        row = []
        for j in range(N):
            if j > i:
                row.append(0.0)                       # causal mask
                continue
            sink = 0.30 if j == 0 else 0.0
            diag = 0.42 if j == i else 0.0
            local = 0.28 * math.exp(-(i - j) / 2.6)
            row.append(sink + diag + local)
        total = sum(row) or 1.0
        rows.append([v / total for v in row])
    return rows


def build(theme: str) -> str:
    t = THEMES[theme]
    A = attention()
    peak = max(max(r) for r in A)

    mono = "ui-monospace,SFMono-Regular,Menlo,DejaVu Sans Mono,monospace"
    sans = "Inter,Segoe UI,Helvetica Neue,DejaVu Sans,sans-serif"

    o: list[str] = []
    add = o.append

    add(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="Divyansh Rai, AI Engineer. A causal attention matrix. '
        f'Open source: mnemos, toolcontract, mapcraft.">'
    )

    add("<defs>")
    add(
        f'<linearGradient id="sweep" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{t["accent"]}" stop-opacity="0"/>'
        f'<stop offset="0.5" stop-color="{t["accent"]}" stop-opacity="0.14"/>'
        f'<stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></linearGradient>'
    )
    add(
        f'<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{t["accent"]}" stop-opacity="0.95"/>'
        f'<stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></linearGradient>'
    )
    add("</defs>")

    add(f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>')

    # ---------------------------------------------------------------- type
    add(
        f'<text x="80" y="116" font-family="{mono}" font-size="12" fill="{t["accent"]}" '
        f'letter-spacing="6">AI ENGINEER</text>'
    )
    add(
        f'<text x="78" y="180" font-family="{sans}" font-size="58" font-weight="700" '
        f'fill="{t["ink"]}" letter-spacing="-1.5">Divyansh Rai</text>'
    )
    # Rule breathes between two widths; never zero, so it is always present.
    add(
        f'<rect x="80" y="200" width="140" height="2" fill="url(#rule)">'
        f'<animate attributeName="width" values="140;320;140" dur="6.5s" '
        f'repeatCount="indefinite"/></rect>'
    )
    add(
        f'<text x="80" y="238" font-family="{sans}" font-size="15.5" fill="{t["dim"]}">'
        f'LLM &amp; VLM fine-tuning · multi-agent systems · RAG · production GenAI</text>'
    )

    # Projects as quiet terminal entries rather than pill buttons.
    for k, (name, x) in enumerate([("mnemos", 80), ("toolcontract", 212), ("mapcraft", 392)]):
        add(
            f'<circle cx="{x + 4}" cy="276" r="3.5" fill="{t["accent"]}">'
            f'<animate attributeName="opacity" values="1;0.28;1" dur="3.2s" '
            f'begin="{k * 1.05:.2f}s" repeatCount="indefinite"/></circle>'
        )
        add(
            f'<text x="{x + 16}" y="281" font-family="{mono}" font-size="13.5" '
            f'fill="{t["ink"]}">{name}</text>'
        )
    add(
        f'<text x="524" y="281" font-family="{mono}" font-size="12" '
        f'fill="{t["faint"]}">— open source</text>'
    )

    # -------------------------------------------------------------- matrix
    add(
        f'<rect x="{GX - 24}" y="{GY - 24}" width="{GRID + 48}" height="{GRID + 48}" '
        f'rx="12" fill="{t["panel"]}" stroke="{t["rule"]}"/>'
    )

    # The masked half is drawn as empty cells rather than left blank. A real
    # attention plot shows the full square with the mask visible, and it stops
    # the panel reading as a triangle floating in dead space.
    for i in range(N):
        for j in range(i + 1, N):
            add(
                f'<rect x="{GX + j * (CELL + GAP):.1f}" y="{GY + i * (CELL + GAP):.1f}" '
                f'width="{CELL}" height="{CELL}" rx="2" fill="none" '
                f'stroke="{t["rule"]}" stroke-width="1"/>'
            )

    # Resting state: the true weights, quietly.
    for i in range(N):
        for j in range(i + 1):
            v = A[i][j] / peak
            add(
                f'<rect x="{GX + j * (CELL + GAP):.1f}" y="{GY + i * (CELL + GAP):.1f}" '
                f'width="{CELL}" height="{CELL}" rx="2" fill="{t["accent"]}" '
                f'opacity="{0.09 + 0.40 * v:.3f}"/>'
            )

    # Query sweep: one row at a time brightens to its real distribution.
    # Eighteen animated groups rather than three hundred animated cells.
    period = 7.2
    step = period / N
    for i in range(N):
        add(
            f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" '
            f'keyTimes="0;0.10;0.55;1" dur="{step * 3.4:.2f}s" '
            f'begin="{i * step:.2f}s" repeatCount="indefinite"/>'
        )
        for j in range(i + 1):
            v = A[i][j] / peak
            add(
                f'<rect x="{GX + j * (CELL + GAP):.1f}" y="{GY + i * (CELL + GAP):.1f}" '
                f'width="{CELL}" height="{CELL}" rx="2" fill="{t["accent"]}" '
                f'opacity="{0.22 + 0.78 * v:.3f}"/>'
            )
        add(
            f'<rect x="{GX - 15:.1f}" y="{GY + i * (CELL + GAP):.1f}" width="5" '
            f'height="{CELL}" rx="2.5" fill="{t["warm"]}"/></g>'
        )

    # Soft band travelling with the sweep, tying the motion together.
    add(
        f'<rect x="{GX - 24}" y="{GY - 44}" width="{GRID + 48}" height="44" '
        f'fill="url(#sweep)"><animate attributeName="y" '
        f'values="{GY - 44};{GY + GRID}" dur="{period}s" repeatCount="indefinite"/></rect>'
    )

    add(
        f'<text x="{GX - 24}" y="{GY - 34}" font-family="{mono}" font-size="10.5" '
        f'fill="{t["faint"]}" letter-spacing="2">KEYS →</text>'
    )
    add(
        f'<text x="{GX - 24}" y="{GY + GRID + 38}" font-family="{mono}" font-size="10.5" '
        f'fill="{t["faint"]}" letter-spacing="1.5">causal self-attention</text>'
    )

    add("</svg>")
    return "".join(o)


if __name__ == "__main__":
    here = pathlib.Path(__file__).parent
    for name in ("dark", "light"):
        p = here / f"banner-{name}.svg"
        p.write_text(build(name), encoding="utf-8")
        print(f"  {p.name}  {p.stat().st_size / 1024:.1f} KB")
