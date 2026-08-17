"""Generate the animated profile banner.

Pure SMIL, no CSS or JS, because GitHub serves the file as an image and only
SMIL is guaranteed to run there. Every element is drawn visible and animation
is layered on top — if the animation does not run, the banner still reads
correctly rather than disappearing.

The right-hand figure is the inference path an agent request actually takes:
tokens arrive, retrieval fires, the model runs, the agent layer acts, and a
response leaves. The particles move in that direction on purpose.
"""

from __future__ import annotations

import pathlib

W, H = 1200, 340

THEMES = {
    "dark": dict(
        bg0="#0b1015", bg1="#161f29",
        ink="#f3f5f7", dim="#94a1ad", faint="#5d6a77",
        teal="#0cc3c3", purple="#9d7bff", amber="#f0b23f",
        grid="#1e2a36", plane_base="#1b2733",
    ),
    "light": dict(
        bg0="#ffffff", bg1="#eef2f6",
        ink="#0f1720", dim="#5d6a77", faint="#94a1ad",
        teal="#0f7f80", purple="#6d4bd6", amber="#b5731a",
        grid="#d8e0e8", plane_base="#dfe7ee",
    ),
}

# Isometric stack: three rhombi, bottom is retrieval, top is agents. Data
# flows upward through them, which is the order a request is actually served.
CX, PLANE_W, PLANE_H = 872, 158, 76
LAYERS = [
    dict(cy=252, key="teal",   label="Retrieval", sub="pgvector · BM25"),
    dict(cy=176, key="purple", label="Model",     sub="LLM · VLM"),
    dict(cy=100, key="amber",  label="Agents",    sub="tools · memory"),
]


def rhombus(cx: float, cy: float, w: float, h: float) -> str:
    return f"{cx},{cy - h / 2} {cx + w},{cy} {cx},{cy + h / 2} {cx - w},{cy}"


def build(theme_name: str) -> str:
    t = THEMES[theme_name]
    o: list[str] = []
    add = o.append

    add(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" fill="none" '
        f'aria-label="Divyansh Rai, AI Engineer. An inference pipeline: retrieval, '
        f'model, and agent layers. Open source: mnemos, toolcontract, mapcraft.">'
    )

    # ---- defs -----------------------------------------------------------
    add("<defs>")
    add(
        f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{t["bg0"]}"/>'
        f'<stop offset="1" stop-color="{t["bg1"]}"/></linearGradient>'
    )
    for key in ("teal", "purple", "amber"):
        c = t[key]
        add(
            f'<linearGradient id="pl-{key}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{t["plane_base"]}" stop-opacity="0.9"/>'
            f'<stop offset="1" stop-color="{c}" stop-opacity="0.38"/></linearGradient>'
        )
        add(
            f'<radialGradient id="gl-{key}" cx="0.5" cy="0.5" r="0.5">'
            f'<stop offset="0" stop-color="{c}" stop-opacity="0.34"/>'
            f'<stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
        )
    # Soft vignette so the figure sits in light rather than on a flat field.
    add(
        f'<radialGradient id="halo" cx="0.72" cy="0.42" r="0.55">'
        f'<stop offset="0" stop-color="{t["teal"]}" stop-opacity="0.10"/>'
        f'<stop offset="1" stop-color="{t["teal"]}" stop-opacity="0"/></radialGradient>'
    )
    add(
        f'<pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse">'
        f'<path d="M34 0H0V34" fill="none" stroke="{t["grid"]}" stroke-width="1" '
        f'stroke-opacity="0.5"/></pattern>'
    )
    add("</defs>")

    # ---- background -----------------------------------------------------
    add(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    # The grid drifts one tile and repeats, so the loop is seamless.
    add(
        f'<g opacity="0.5"><rect x="-34" y="-34" width="{W + 68}" height="{H + 68}" fill="url(#grid)">'
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="0 0; 34 34" dur="9s" repeatCount="indefinite"/></rect></g>'
    )
    add(f'<rect width="{W}" height="{H}" fill="url(#halo)"/>')

    # ---- left column ----------------------------------------------------
    mono = "ui-monospace,SFMono-Regular,Menlo,DejaVu Sans Mono,monospace"
    sans = "Verdana,DejaVu Sans,sans-serif"

    add(
        f'<text x="64" y="96" font-family="{mono}" font-size="14" fill="{t["teal"]}" '
        f'letter-spacing="4">$ whoami</text>'
    )
    add(
        f'<text x="64" y="160" font-family="{sans}" font-size="54" font-weight="bold" '
        f'fill="{t["ink"]}">Divyansh Rai</text>'
    )
    add(
        f'<text x="64" y="198" font-family="{sans}" font-size="21" font-weight="bold" '
        f'fill="{t["teal"]}">AI Engineer</text>'
    )
    add(
        f'<text x="64" y="234" font-family="{sans}" font-size="14.5" fill="{t["dim"]}">'
        f'LLM / VLM fine-tuning · multi-agent systems · RAG · production GenAI</text>'
    )

    # Project pills. Drawn visible; only the dot pulses.
    pills = [
        ("mnemos", "teal", 64, 108),
        ("toolcontract", "purple", 184, 152),
        ("mapcraft", "amber", 348, 118),
    ]
    for i, (label, key, x, w) in enumerate(pills):
        c = t[key]
        add(
            f'<g><rect x="{x}" y="260" width="{w}" height="34" rx="17" fill="{c}" '
            f'fill-opacity="0.13" stroke="{c}" stroke-opacity="0.5"/>'
            f'<circle cx="{x + 22}" cy="277" r="5" fill="{c}">'
            f'<animate attributeName="opacity" values="1;0.25;1" dur="2.8s" '
            f'begin="{i * 0.55:.2f}s" repeatCount="indefinite"/></circle>'
            f'<text x="{x + 38}" y="282" font-family="{mono}" font-size="13" '
            f'font-weight="bold" fill="{c}">{label}</text></g>'
        )
    add(
        f'<text x="482" y="282" font-family="{mono}" font-size="12.5" '
        f'fill="{t["faint"]}">open source</text>'
    )

    # ---- inference figure ------------------------------------------------
    bottom, top = LAYERS[0]["cy"], LAYERS[-1]["cy"]

    for i, layer in enumerate(LAYERS):
        c = t[layer["key"]]
        cy = layer["cy"]
        begin = f"{i * 0.7:.2f}s"

        # Glow beneath each plane, breathing in sequence up the stack.
        add(
            f'<ellipse cx="{CX}" cy="{cy}" rx="{PLANE_W * 1.15}" ry="{PLANE_H * 0.95}" '
            f'fill="url(#gl-{layer["key"]})">'
            f'<animate attributeName="opacity" values="0.55;1;0.55" dur="3.4s" '
            f'begin="{begin}" repeatCount="indefinite"/></ellipse>'
        )
        # The plane itself, lifting a couple of pixels on the same cadence.
        add(
            f'<g><animateTransform attributeName="transform" type="translate" '
            f'values="0 0; 0 -3; 0 0" dur="3.4s" begin="{begin}" repeatCount="indefinite"/>'
            f'<polygon points="{rhombus(CX, cy, PLANE_W, PLANE_H)}" '
            f'fill="url(#pl-{layer["key"]})" stroke="{c}" stroke-opacity="0.75" '
            f'stroke-width="1.5"/>'
        )
        # Activation dots scattered on the face, twinkling out of phase.
        for j, (dx, dy) in enumerate(
            [(-70, 0), (-35, -14), (0, 0), (35, 14), (70, 0), (-35, 14), (35, -14), (0, -22), (0, 22)]
        ):
            add(
                f'<circle cx="{CX + dx}" cy="{cy + dy}" r="2.4" fill="{c}" opacity="0.85">'
                f'<animate attributeName="opacity" values="0.85;0.2;0.85" dur="2.2s" '
                f'begin="{(i * 0.7 + j * 0.18):.2f}s" repeatCount="indefinite"/></circle>'
            )
        add("</g>")

        # Leader line out to the label.
        add(
            f'<line x1="{CX + PLANE_W}" y1="{cy}" x2="{CX + PLANE_W + 42}" y2="{cy}" '
            f'stroke="{c}" stroke-opacity="0.5" stroke-width="1.5"/>'
        )
        add(f'<circle cx="{CX + PLANE_W + 42}" cy="{cy}" r="3.5" fill="{c}"/>')
        add(
            f'<text x="{CX + PLANE_W + 54}" y="{cy - 2}" font-family="{sans}" '
            f'font-size="13" font-weight="bold" fill="{c}">{layer["label"]}</text>'
        )
        add(
            f'<text x="{CX + PLANE_W + 54}" y="{cy + 14}" font-family="{mono}" '
            f'font-size="10.5" fill="{t["faint"]}">{layer["sub"]}</text>'
        )

    # Drawn after the planes so the flow reads on top of them rather than
    # being painted over by the geometry it is meant to pass through.
    add(
        f'<line x1="{CX}" y1="{bottom}" x2="{CX}" y2="{top}" stroke="{t["teal"]}" '
        f'stroke-opacity="0.35" stroke-width="1.5" stroke-dasharray="4 6">'
        f'<animate attributeName="stroke-dashoffset" values="20;0" dur="1.6s" '
        f'repeatCount="indefinite"/></line>'
    )

    # Particles climbing the spine: retrieval -> model -> agents.
    for k in range(5):
        add(
            f'<circle r="4" fill="{t["teal"]}" stroke="{t["bg0"]}" stroke-width="1.2" opacity="0">'
            f'<animate attributeName="cy" values="{bottom};{top}" dur="2.8s" '
            f'begin="{k * 0.56:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="cx" values="{CX};{CX}" dur="2.8s" '
            f'begin="{k * 0.56:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.12;0.8;1" '
            f'dur="2.8s" begin="{k * 0.56:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="fill" values="{t["teal"]};{t["purple"]};{t["amber"]}" '
            f'dur="2.8s" begin="{k * 0.56:.2f}s" repeatCount="indefinite"/></circle>'
        )

    # Token stream arriving from the left, so the figure reads as a pipeline
    # with an input rather than a static diagram.
    for k in range(6):
        add(
            f'<rect y="{bottom - 3}" width="14" height="4" rx="2" fill="{t["teal"]}" opacity="0">'
            f'<animate attributeName="x" values="640;{CX - PLANE_W - 10}" dur="2.4s" '
            f'begin="{k * 0.4:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.9;0" dur="2.4s" '
            f'begin="{k * 0.4:.2f}s" repeatCount="indefinite"/></rect>'
        )

    add("</svg>")
    return "".join(o)


if __name__ == "__main__":
    here = pathlib.Path(__file__).parent
    for name in ("dark", "light"):
        path = here / f"banner-{name}.svg"
        path.write_text(build(name), encoding="utf-8")
        print(f"  wrote {path.name}  {path.stat().st_size / 1024:.1f} KB")
