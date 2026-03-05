# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.20.4",
# ]
# ///
import marimo as mo
import pandas as pd
import plotly.io as pio

def _callout(kind: str, content: str):
    css_class = "callout-danger" if kind == "danger" else "callout-info"
    return mo.Html(f"<div class='{css_class}'>{content}</div>")

def callout_info(content: str):
    return _callout("info", content)

def callout_danger(content: str):
    return _callout("danger", content)

async def gh_pages_read_csv_into_df(filename: str) -> pd.DataFrame:
    filepath = mo.notebook_location() / "public" / filename
    if "http" not in str(mo.notebook_location()):
        return pd.read_csv(
            filepath, 
            index_col=0
        )
    from pyodide.http import pyfetch
    from io import StringIO
    response = await pyfetch(filepath)
    data = await response.text()
    return pd.read_csv(StringIO(data))

COLOR_PALETTE = [
        "#4442e3", # 1. Brand Blue
        "#ffb60c", # 2. Brand Yellow
        "#ff584e", # 3. Brand Coral
        "#10b981", # 4. Method Green
        "#8b89f5", # 5. Vibrant Periwinkle
        "#2b298c", # 6. Deep Navy
        "#0ea5e9", # 7. Electric Teal
        "#f97316", # 8. Vibrant Orange
        "#ff9e99", # 9. Soft Melon
        "#4e4e4e"  # 10. Method Slate
]

def run_plotly_defaults():
    pio.templates.default = "plotly_white"
    pio.templates["plotly_white"].layout.margin = dict(t=0, b=0)
    pio.templates["plotly_white"].layout.font.family = "var(--marimo-text-font)"
    pio.templates["plotly_white"].layout.title.font.family = "var(--marimo-text-font)"
    for renderer_name in pio.renderers.default.split("+"):
        renderer_name = renderer_name.strip()
        if not renderer_name:
            continue
        if renderer_name not in pio.renderers:
            continue
        renderer = pio.renderers[renderer_name]
        if hasattr(renderer, "config") and renderer.config is not None:
            renderer.config["displayModeBar"] = False