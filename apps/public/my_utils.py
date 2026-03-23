# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.20.4",
# ]
# ///
import marimo as mo
import pandas as pd
import plotly.io as pio
from decimal import Decimal

def _callout(kind: str, content: str):
    css_class = f"callout-{kind}"
    return mo.Html(f"<div class='{css_class}'>{content}</div>")

def callout_neutral(content: str):
    return _callout("neutral", content)

def callout_info(content: str):
    return _callout("info", content)

def callout_danger(content: str):
    return _callout("danger", content)

def callout_warning(content: str):
    return _callout("warning", content)

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

async def gh_pages_load_image(filename: str) -> pd.DataFrame:
    filepath = mo.notebook_location() / "public" / filename
    if "http" not in str(mo.notebook_location()):
        return mo.image(filepath)
    from pyodide.http import pyfetch
    from io import BytesIO
    response = await pyfetch(filepath)
    data = await response.bytes()
    return mo.image(BytesIO(data))

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
    "#4e4e4e", # 10. Method Slate
    "#ec4899"  # 11. Vibrant Pink
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

def title_with_icon(value: int, cutoff_value: int, title: str, subtitle:str = "", yes_icon:str = "☑️", no_icon:str = "❌", yes_color:str = COLOR_PALETTE[0], no_color:str = COLOR_PALETTE[2]):
    _heading_icon = yes_icon if value <= cutoff_value else no_icon
    _heading_color = yes_color if value <= cutoff_value else no_color
    return mo.md(f"""
    ### {_heading_icon} <span style="color: {_heading_color};"> <b>{title}</b>{f" {subtitle}" if subtitle else ""}</span>
    """)

def round_num(n, decimal=2):
    n=Decimal(n)
    return n.to_integral() if n == n.to_integral() else round(n.normalize(), decimal)

def numerize(n, decimal=2):
    #60 sufixes
    sufixes = [ "", "K", "M", "B", "T", "Qa", "Qu", "S", "Oc", "No", 
                "D", "Ud", "Dd", "Td", "Qt", "Qi", "Se", "Od", "Nd","V", 
                "Uv", "Dv", "Tv", "Qv", "Qx", "Sx", "Ox", "Nx", "Tn", "Qa",
                "Qu", "S", "Oc", "No", "D", "Ud", "Dd", "Td", "Qt", "Qi",
                "Se", "Od", "Nd", "V", "Uv", "Dv", "Tv", "Qv", "Qx", "Sx",
                "Ox", "Nx", "Tn", "x", "xx", "xxx", "X", "XX", "XXX", "END"] 
    
    sci_expr = [1e0, 1e3, 1e6, 1e9, 1e12, 1e15, 1e18, 1e21, 1e24, 1e27, 
                1e30, 1e33, 1e36, 1e39, 1e42, 1e45, 1e48, 1e51, 1e54, 1e57, 
                1e60, 1e63, 1e66, 1e69, 1e72, 1e75, 1e78, 1e81, 1e84, 1e87, 
                1e90, 1e93, 1e96, 1e99, 1e102, 1e105, 1e108, 1e111, 1e114, 1e117, 
                1e120, 1e123, 1e126, 1e129, 1e132, 1e135, 1e138, 1e141, 1e144, 1e147, 
                1e150, 1e153, 1e156, 1e159, 1e162, 1e165, 1e168, 1e171, 1e174, 1e177]
    minus_buff = n
    n=abs(n)
    for x in range(len(sci_expr)):
        try:
            if n >= sci_expr[x] and n < sci_expr[x+1]:
                sufix = sufixes[x]
                if n >= 1e3:
                    num = str(round_num(n/sci_expr[x], decimal))
                else:
                    num = str(n)
                return num + sufix if minus_buff > 0 else "-" + num + sufix
        except IndexError:
            print("You've reached the end")