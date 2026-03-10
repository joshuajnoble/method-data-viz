# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.20.2",
#     "plotly",
#     "pandas",
#     "openai==2.26.0",
#     "pydantic-ai-slim==1.67.0",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium", css_file="custom.css")

with app.setup(hide_code=True):
    # imports
    import plotly.express as px
    import pandas as pd
    import marimo as mo


@app.cell(hide_code=True)
async def setup_wasm():
    import sys
    import types
    import importlib.util
    from pathlib import Path

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
    return (my_utils,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Types of Visualizations

    TODO: summary

    Covering vertical bar charts, line charts, and pie charts
    """)
    return


@app.cell(hide_code=True)
async def _(my_utils):
    # prep data
    base_df = await my_utils.gh_pages_read_csv_into_df("superstore.csv")

    base_df_with_year = base_df.assign(
        _order_year=pd.to_datetime(base_df["Order Date"], format="%m/%d/%y").dt.year
    )
    segment_year_sales_df = (
        base_df_with_year.groupby(["_order_year", "Sub-Category"], as_index=False)["Sales"]
        .sum()
        .rename(columns={"_order_year": "Year","Sub-Category":"Category"})
    )
    return base_df, segment_year_sales_df


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Vertical Bar Charts

    Consider a vertical bar chart of many categories. Depending on what story you're looking to tell, there are usually two ways to group the bars.
    """)
    return


@app.cell(hide_code=True)
async def _(my_utils):
    _img = await my_utils.gh_pages_load_image("grouped_bar.jpg")
    mo.hstack([_img,mo.md("**Grouped or Clustered Bar Chart**: In this format, bars representing different categories are placed side by side for each group (e.g., year). This allows for easy *comparison of categories within the same group/cluster* while still getting a sense for the overall trend. However, if there are too many categories, it can become *visually overwhelming* and difficult to interpret.")],gap=2,align="center",widths=[.25,1])
    return


@app.cell
async def _(my_utils):
    _img = await my_utils.gh_pages_load_image("small_multiples.jpg")
    mo.hstack([_img,mo.md("**Small Multiples**: In this format, each category gets its own individual chart (or subplot) that shares the same axes. This allows for *easier comparison of trends across categories* without the visual clutter of a grouped bar chart. However, it can be more difficult to compare values across categories since they are not visually grouped together. Tip: consider adding darker axis lines to allow easier comparison across groups.")],gap=2,align="center",widths=[.25,1])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    **The slider below** 👇 changes the number of categories shown in the associated chart. Experiment with which chart type might be the most effective for the **number of categories** as they relate to the **goal of the visual**. How might you focus the experience on showing **intra-year comparisons** vs. **individual trends**?
    """)
    return


@app.cell
def _():
    mo.Html("<hr>")
    return


@app.cell(hide_code=True)
def _():
    chart_slider = mo.ui.slider(
        start=1,
        stop=10,
        value=3,
        label="Number of categories",
        show_value = True,
        full_width=True
    )
    return (chart_slider,)


@app.cell
def callout_barchart(chart_slider, my_utils):
    # callout
    _message_by_range = [
        {"min": 1, "max": 3, "message": my_utils.callout_info("<b>1-3 categories</b>: This number of categories is typically manageable in a <b>grouped bar chart</b>. It focuses on <b>intra-year comparisons of categories</b> and allows for comparison of an individual category's value across the whole timeline. <b>Small multiples</b> (below) will also work well and can help to emphasize <b>individual category trends</b>.")},
        {"min": 4, "max": 7, "message": my_utils.callout_danger("<b>4-7 categories</b>: This number of categories is on the higher end for a <b>grouped bar chart</b> and can introduce <b>visual overwhelm</b>. Consider <b>small multiples</b> (below) to enable comparing <b>individual trends</b> across categories.")},
        {"min": 8, "max": float("inf"), "message": my_utils.callout_danger("<b>8+ categories</b>: This number of categories will introduce <b>visual overwhelm with either chart type</b>. If you need more than 7 categories, try <b>consolidating categories or providing a table view instead.</b>")},
    ]

    _message = next(
        item["message"]
        for item in _message_by_range
        if item["min"] <= chart_slider.value <= item["max"]
    ) 

    mo.hstack([_message,chart_slider],gap=2,align="center",widths=[2,.75])
    return


@app.cell(hide_code=True)
def _(chart_slider, my_utils):
    _heading_color = my_utils.COLOR_PALETTE[0] if 1 <= chart_slider.value <= 3 else  my_utils.COLOR_PALETTE[2]
    mo.md(
        f"""
    ### <span style="color: {_heading_color};">**Grouped Bar Chart** (Category Sales by Year)</span>
    """
    )
    return


@app.cell(hide_code=True)
def _(chart_slider, my_utils, segment_year_sales_df):
    top_subcats = (
        segment_year_sales_df.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(chart_slider.value)["Category"]
    )

    filtered_segment_year_sales_df = segment_year_sales_df[
        segment_year_sales_df["Category"].isin(top_subcats)
    ]

    bar_fig = px.bar(
        filtered_segment_year_sales_df,
        x="Year",
        y="Sales",
        color="Category",
        barmode="group",
        color_discrete_sequence=my_utils.COLOR_PALETTE[:len(top_subcats)]
    )

    _year_ticks = sorted(filtered_segment_year_sales_df["Year"].unique())
    bar_fig.update_xaxes(
        tickmode="array",
        tickvals=_year_ticks,
        ticktext=_year_ticks
    )
    bar_fig.update_yaxes(tickformat="$,.0f", gridcolor="rgba(0, 0, 0, 0.15)",
        gridwidth=1.1)
    bar_fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            title = "",
            xanchor="left",
            x=0,
            font=dict(size=14),
        ),
        height=400,
    )
    mo.ui.plotly(bar_fig, config={"displayModeBar": False})
    return


@app.cell
def _():
    mo.Html("<hr>")
    return


@app.cell
def _(chart_slider, my_utils):
    # callout
    _message_by_range = [
        {"min": 1, "max": 3, "message": my_utils.callout_info("<b>1-3 categories</b>: This number of categories is also well-suited for a <b>small multiples chart</b>. It focuses on <b>yearly trend</b> of an individual category while still allowing for comparison against other categories. <b>Grouped bar charts</b> (above) also work well for this number of categories and can help to emphasize <b>intra-year comparisons</b>.")},
        {"min": 4, "max": 7, "message": my_utils.callout_info("<b>4-7 categories</b>: This number of categories is great for a <b>small multiples chart</b> and showing <b>individual trends</b> while still allowing for comparison across categories.")},
        {"min": 8, "max": float("inf"), "message": my_utils.callout_danger("<b>8+ categories</b>: This number of categories will introduce <b>visual overwhelm with either chart type</b>. If you need more than 7 categories, try <b>consolidating categories or providing a table view instead.</b>")},
    ]

    _message = next(
        item["message"]
        for item in _message_by_range
        if item["min"] <= chart_slider.value <= item["max"]
    ) 

    mo.hstack([_message,chart_slider],gap=2,align="center",widths=[2,.75])
    return


@app.cell(hide_code=True)
def _(chart_slider, my_utils):
    _heading_color = my_utils.COLOR_PALETTE[0] if 1 <= chart_slider.value <= 7 else  my_utils.COLOR_PALETTE[2]
    mo.md(
        f"""
    ### <span style="color: {_heading_color};">**Small Multiples** (Yearly Sales by Category)</span>
    """
    )
    return


@app.cell(hide_code=True)
def _(chart_slider, my_utils, segment_year_sales_df):
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    segment_year_sales_df_with_year_cat = segment_year_sales_df.assign(
        Year=segment_year_sales_df["Year"].astype(str)
    )

    top_categories = (
        segment_year_sales_df_with_year_cat.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(chart_slider.value)["Category"]
    )

    filtered_category_sales_df = segment_year_sales_df_with_year_cat[
        segment_year_sales_df_with_year_cat["Category"].isin(top_categories)
    ]

    years = sorted(filtered_category_sales_df["Year"].unique())
    categories = sorted(top_categories.tolist())
    category_colors = {
        category: my_utils.COLOR_PALETTE[i % len(my_utils.COLOR_PALETTE)]
        for i, category in enumerate(categories)
    }

    category_sales_subplots_fig = make_subplots(
        rows=1,
        cols=len(categories),
        shared_yaxes=True,
        subplot_titles=categories,
    )

    for _col_idx, _category in enumerate(categories, start=1):
        _category_df = filtered_category_sales_df[
            filtered_category_sales_df["Category"] == _category
        ].sort_values("Year")
        for year in years:
            _year_value = _category_df[_category_df["Year"] == year]
            category_sales_subplots_fig.add_trace(
                go.Bar(
                    x=_year_value["Year"],
                    y=_year_value["Sales"],
                    name=_category,
                    marker_color=category_colors[_category],
                    showlegend=_col_idx == 1 and year == years[0],
                ),
                row=1,
                col=_col_idx,
            )

    category_sales_subplots_fig.update_yaxes(tickformat="$,.0f", title="", gridcolor="rgba(0, 0, 0, 0.15)",gridwidth=1.05)
    category_sales_subplots_fig.update_xaxes(title="")
    category_sales_subplots_fig.update_layout(barmode="group",
                                              showlegend=False,
                                              margin = dict(t=30),
                                              height=400)
    category_sales_subplots_fig.update_annotations(font_size=14)
    mo.ui.plotly(category_sales_subplots_fig, config={"displayModeBar": False})
    return go, make_subplots, segment_year_sales_df_with_year_cat


@app.cell
def _():
    mo.Html("<hr>")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Line Charts
    """)
    return


@app.cell
def _(my_utils):
    line_chart_slider = mo.ui.slider(
        start=1,
        stop=7,
        value=3,
        label="Number of categories",
        show_value = True,
        full_width=True
    )

    mo.center(line_chart_slider)

    _message = my_utils.callout_neutral("Similarly, consider a <b>line chart</b> of the same information. How does the choice between a single line chart with <b>all categories</b> vs. <b>small multiples</b> of line charts affect your ability to <b>compare trends</b> across categories and within categories? Does the number of categories shown change <b>which chart type is more effective</b> for the story you're trying to tell with the data?")

    mo.hstack([_message,line_chart_slider],gap=2,align="center",widths=[2,.75])
    return (line_chart_slider,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### **Overlapping** (Yearly Sales by Category)
    """)
    return


@app.cell
def _():
    fig_switch = mo.ui.switch(value=False, label="*Highlighting a single category within many overlapping lines can focus the story.*")
    return (fig_switch,)


@app.cell
def _(fig_switch):
    fig_switch
    return


@app.cell(hide_code=True)
def _(
    fig_switch,
    line_chart_slider,
    my_utils,
    segment_year_sales_df_with_year_cat,
):
    line_top_categories = (
        segment_year_sales_df_with_year_cat.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(line_chart_slider.value)["Category"]
    )

    line_filtered_category_sales_df = segment_year_sales_df_with_year_cat[
        segment_year_sales_df_with_year_cat["Category"].isin(line_top_categories)
    ]

    line_years = sorted(line_filtered_category_sales_df["Year"].unique())
    line_categories = sorted(line_top_categories.tolist())
    line_category_colors = {
        category: my_utils.COLOR_PALETTE[i % len(my_utils.COLOR_PALETTE)]
        for i, category in enumerate(line_categories)
    }


    line_all_categories_fig = px.line(
        line_filtered_category_sales_df,
        x="Year",
        y="Sales",
        color="Category",
        markers=True,
        title="",
        color_discrete_sequence=my_utils.COLOR_PALETTE[:len(line_categories)]
    )
    line_all_categories_fig.update_yaxes(tickformat="$,.0f",rangemode="tozero")
    line_all_categories_fig.update_xaxes(title="")
    line_all_categories_fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            title = "",
            xanchor="left",
            x=0,
            font=dict(size=14),
        ),
        height=400,
    )




    first_category = line_categories[0] if len(line_categories) > 0 else None

    line_highlight_fig = px.line(
        line_filtered_category_sales_df,
        x="Year",
        y="Sales",
        color="Category",
        markers=True,
    )

    for trace in line_highlight_fig.data:
        if trace.name == first_category:
            trace.update(line=dict(color=line_category_colors[first_category], width=3), marker=dict(color=line_category_colors[first_category], size=9))
        else:
            trace.update(line=dict(color="rgba(160, 160, 160, 0.7)", width=2), marker=dict(color="rgba(160, 160, 160, 0.7)", size=6))

    line_highlight_fig.update_yaxes(tickformat="$,.0f", rangemode="tozero")
    line_highlight_fig.update_xaxes(title="")
    line_highlight_fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            title="",
            xanchor="left",
            x=0,
            font=dict(size=14),
        ),
        height=400,
    )

    # Cell B: choose which already-prepared figure to show
    _selected_line_fig = line_highlight_fig if fig_switch.value else line_all_categories_fig
    mo.ui.plotly(_selected_line_fig,config={"displayModeBar": False})
    return (
        line_categories,
        line_category_colors,
        line_filtered_category_sales_df,
    )


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### **Small Multiples** (Category Sales by Year)
    """)
    return


@app.cell(hide_code=True)
def _(
    go,
    line_categories,
    line_category_colors,
    line_filtered_category_sales_df,
    make_subplots,
):
    line_category_sales_subplots_fig = make_subplots(
        rows=1,
        cols=len(line_categories),
        shared_yaxes=True,
        subplot_titles=line_categories,
    )

    for _col_idx, _category in enumerate(line_categories, start=1):
        _category_df = line_filtered_category_sales_df[
            line_filtered_category_sales_df["Category"] == _category
        ].sort_values("Year")
        line_category_sales_subplots_fig.add_trace(
            go.Scatter(
                x=_category_df["Year"],
                y=_category_df["Sales"],
                mode="lines+markers",
                name=_category,
                line=dict(color=line_category_colors[_category]),
                marker=dict(color=line_category_colors[_category]),
                showlegend=False,
            ),
            row=1,
            col=_col_idx,
        )

    line_category_sales_subplots_fig.update_yaxes(tickformat="$,.0f", title="", rangemode="tozero")
    line_category_sales_subplots_fig.update_xaxes(title="")
    line_category_sales_subplots_fig.update_layout(barmode="group",
                                              showlegend=False,
                                              margin = dict(t=30),
                                              height=400)
    line_category_sales_subplots_fig.update_annotations(font_size=14)
    mo.ui.plotly(line_category_sales_subplots_fig,config={"displayModeBar": False})
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Pie Charts

    Pie charts are great for showing how a total is divided into parts, especially when you want to emphasize the proportion of each category to the whole. However, they can become difficult to interpret with too many categories or similar values. Consider using a pie chart when you have a small number of categories (ideally 5 or fewer) and when the goal is to show the relative contribution of each category to the total. For larger numbers of categories, consider alternative visualizations like a stacked bar chart.

    TODO: direct labeling.
    """)
    return


@app.cell
def _():
    category_slider = mo.ui.slider(start=2, stop=10, value=5, label = "Number of categories", show_value = True)
    category_slider
    return (category_slider,)


@app.cell
def _(base_df, category_slider):
    segment_sales_df = (
        base_df.groupby(["Sub-Category"], as_index=False)["Sales"]
        .sum()
        .rename(columns={"Sub-Category":"Category"})
        #.sort_values(by="Sales", ascending=False)
        .head(category_slider.value)
        .sort_values(by="Sales", ascending=False)
    )
    return (segment_sales_df,)


@app.cell
def _(category_slider, my_utils, segment_sales_df):
    _total_sales = segment_sales_df["Sales"].sum()
    _heading_icon = "☑️" if 1 <= category_slider.value <= 5 else "❌"
    _heading_color = my_utils.COLOR_PALETTE[0] if 1 <= category_slider.value <= 5 else  my_utils.COLOR_PALETTE[2]
    mo.md(f"""
    ### {_heading_icon} <span style="color: {_heading_color};"> <b>Pie Chart</b> (Category Sales Split, Total: ${_total_sales / 1_000_000:,.2f}M)</span>
    """)

    return


@app.cell
def _(category_slider, my_utils, segment_sales_df):
    import plotly.express as _px  

    _pie_fig = _px.pie(
        segment_sales_df,
        names="Category",
        values="Sales",
        title="",
        color="Category",
        color_discrete_sequence=my_utils.COLOR_PALETTE[:category_slider.value]
    )
    _pie_fig.update_traces(textposition="inside", textinfo="percent+label", hovertemplate="%{label}: %{value} (%{percent})<extra></extra>")
    _pie_fig.update_layout(showlegend = False)

    _pie_fig
    return


if __name__ == "__main__":
    app.run()
