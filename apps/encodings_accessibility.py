# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "pandas",
#     "plotly"
# ]
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")

async with app.setup(hide_code=True):
    # imports
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import marimo as mo
    import numpy as np
    from pathlib import Path
    import sys
    import types
    import importlib.util

    module_name = "my_utils"

    if sys.platform == "emscripten":
        from pyodide.http import pyfetch

        print("WASM detected: Fetching local modules...")
        # needs to be ../public because of how the assets dir is created during build
        response = await pyfetch("../public/my_utils.py")
        if not response.ok:
            print("Attempted to fetch:", response.url)
            raise RuntimeError(f"Failed to load my_utils.py. Status: {response.status}")

        source = await response.text()
        module = types.ModuleType(module_name)
        module.__file__ = "/virtual/my_utils.py"
        exec(compile(source, module.__file__, "exec"), module.__dict__)
        sys.modules[module_name] = module
        my_utils = module
        print("Successfully loaded my_utils.py!")
    else:
        # Local Python: load from apps/public/my_utils.py
        module_path = Path("./apps/public/my_utils.py").resolve()
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not load module spec from {module_path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        my_utils = module
        print("Local Python environment detected. Loaded my_utils.py from public/.")

    my_utils.run_plotly_defaults()


@app.cell
def _():
    mo.md("""
    # Encodings aka 'that line means something'


    Visual encoding is the foundational process of mapping data values to visual attributes (position, size, shape, color) to represent information graphically. It translates abstract numbers into visual cues that the human brain can quickly interpret, enabling the comparison and analysis of complex datasets. Some of the most common channels include position, length, area, and color.

    If we look at a simple line graph, the *height* of the line is Life Expectancy (shown on the Y-axis), the *span* of the line is the year being measured (the X-axis), and the *color* of the line is the country (shown in the legend). This is all pretty remedial information but it's worth thinking for a second about why this very simple chart works.
    """)
    return


@app.cell
def _():
    df = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(df, x="year", y="lifeExp", color='country')
    fig.update_layout(xaxis_title="Year", yaxis_title="Life Expectancy in Years")
    fig.show()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    If the two colors were too similar, we couldn't tell the countries apart. If the Y-axis went from 0-1000 or if the range of years were 1000-3000, we wouldn't be able to see the change. The little things that make this simple chart work are the same things that make much more complex and dense charts work as well. The 3D touches on this graphic use basically the same principles:

    ![image](https://i.redd.it/97eipmti3adg1.jpeg)
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Encodings are what make visualizations work.
    """)
    return


@app.cell(hide_code=True)
async def _():
    _img = await my_utils.gh_pages_load_image("encodings/bar_1.png")
    mo.hstack([_img,mo.md("**Highlighting part of a Bar Chart**: Accent color one value and grey out the others")],gap=2,align="center",widths=[.3,.7])
    return


@app.cell
async def _():
    _img = await my_utils.gh_pages_load_image("encodings/bar_2.png")
    mo.hstack([_img,mo.md("**Highlighting two parts of a Bar Chart**: Accent color two values to compare them to the one another other")],gap=2,align="center",widths=[.3,.7])
    return


@app.cell
async def _():
    _img = await my_utils.gh_pages_load_image("encodings/bar_high_disparity.png")
    mo.hstack([_img,mo.md("**Choose the chart type based on the data properties and the charactersitics of the data**: When there are high disparaties between categories, a bar chart can be hard to read. A lot of the bar here isn't doing much.")],gap=2,align="center",widths=[.5,.5])
    return


@app.cell
async def _():
    _img = await my_utils.gh_pages_load_image("encodings/scatter_high_disparity.png")
    mo.hstack([_img,mo.md("**Choose the chart type based on the data properties and the charactersitics of the data**: A scatter plot makes it easier to compare and uses less space to compare the distance between one category and the others.")],gap=2,align="center",widths=[.5,.5])
    return


@app.cell
async def _():
    _img = await my_utils.gh_pages_load_image("encodings/bar_non_zero_x.png")
    mo.hstack([_img,mo.md("**Start at Zero**: Truncating ranges deceives the reader. Here it looks like purple is 8 times greater than grey where as really it's about 2.5 times greater.")],gap=2,align="center",widths=[.5,.5])
    return


@app.cell
async def _():
    _img = await my_utils.gh_pages_load_image("encodings/bar_zero_x.png")
    mo.hstack([_img,mo.md("**Start at Zero**: Beginning at zero keeps it honest. We could start at `$35k` but then we'd lose the insight that purple is about 75% greater than grey.")],gap=2,align="center",widths=[.5,.5])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Colors

    Colors are more than just pretty things, they're informative things.

    A common type of color scale is _continuous_. This makes sense if we're dealing with quantities that can be divided into fractions like degrees in Celsius or measurements of distance.
    """)
    return


@app.cell(hide_code=True)
def _():
    # Create a smooth range
    x = np.linspace(0, 1, 256)
    z = [x]  # 1-row heatmap

    fig_cont = go.Figure(
        data=go.Heatmap(
            z=z,
            colorscale="Viridis",
            showscale=False
        )
    )

    fig_cont.update_layout(
    
        margin=dict(l=0, r=0, t=0, b=0),
        # X-axis cleanup
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            fixedrange=True
        ),

        # Y-axis cleanup
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            fixedrange=True
        ),
        height=100
    )

    fig_cont.show()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    If we break this scale up, then it becomes _discrete_. This makes sense if we're dealing with quantities that can't be divided into fractions, like people or laptops.
    """)
    return


@app.cell
def _():
    x2 = np.linspace(0, 1, 12)
    z2 = [x2]  # 1-row heatmap

    fig_disc1 = go.Figure(
        data=go.Heatmap(
            z=z2,
            colorscale="Viridis",
            showscale=False
        )
    )

    fig_disc1.update_layout(
    
        margin=dict(l=0, r=0, t=0, b=0),
        # X-axis cleanup
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            fixedrange=True
        ),

        # Y-axis cleanup
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            fixedrange=True
        ),
        height=100
    )

    fig_disc1.show()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    There are also _quantitative_ scales, which is how we encode how different things appear. In a bar chart showing sales of different categories of items, we should help readers know which is Computers and which is Jackets. We do this but using a quantitative scale that doesn't go from one color to another across a range, but instead looks very different for each value.
    """)
    return


@app.cell
def _():
    fig_quant = go.Figure()

    w = 1.0

    colors = px.colors.qualitative.Set1
    for i, color in enumerate(colors):
        fig_quant.add_shape(
            type="rect",
            x0=i * w,
            x1=(i+1) * w,
            y0=0,
            y1=100,
            fillcolor=color,
            line=dict(width=0)
        )

    fig_quant.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        # X-axis cleanup
        xaxis=dict(
            range=[0, len(colors)],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            fixedrange=True
        ),

        # Y-axis cleanup
        yaxis=dict(
            range=[0, 1],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            fixedrange=True
        ),

        # Remove background visuals
        plot_bgcolor="white",
        paper_bgcolor="white",
        shapes=dict(layer="below"),
        height=100
    )

    fig_quant.show()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Titles and Labels

    There's more than just colors and shapes to visualization: without good labels saying what values are (and aren't), the story that the chart is trying to tell will get lost or be misinterpreted.
    """)
    return


@app.cell
def _():
    mo.hstack([mo.md("**Use your titles to lead with the story**"), mo.md("\"Monthly Sales by Product, 2021-2025\" <br> vs. <br> \"March and April show seasonal drop in sales for Electronics every year, with 2024 being the worst\"")],gap=2,align="center",widths=[.3,.7])
    return


@app.cell
def _():
    mo.hstack([mo.md("**Use Madlibs dynamic text**"), mo.md("If it's dynamic/autogenerated, try the 'madlibs' approach: <br> **{month_year}** was the best performing month for **{category_x}** <br> like <br> **March 2023** was the best performing month for **Electronics**")],gap=2,align="center",widths=[.3,.7])
    return


@app.cell
def _():
    mo.hstack([mo.md("**Subtitles can (and _should_) add context about data/sources**"), mo.vstack([mo.md("##**March 2023** was the best performing month for **Electronics**"), mo.md("Source: E-commerce database in Salesforce")])],gap=2,align="center",widths=[.3,.7])
    return


if __name__ == "__main__":
    app.run()
