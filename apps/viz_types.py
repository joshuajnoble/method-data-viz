# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.20.2",
#     "plotly",
#     "pandas",
#     "numerize==0.12",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium", css_file="custom.css")

with app.setup(hide_code=True):
    # imports
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import marimo as mo
    from numerize import numerize


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
    my_utils.title_with_icon(value = chart_slider.value, cutoff_value = 3, title = "Grouped Bar Chart", subtitle="(Category Sales by Year)")
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
        text_auto=chart_slider.value <= 5,
        color_discrete_sequence=my_utils.COLOR_PALETTE[:len(top_subcats)]
    )
    bar_fig.update_traces(textposition="outside", cliponaxis=False)

    _year_ticks = sorted(filtered_segment_year_sales_df["Year"].unique())
    bar_fig.update_xaxes(
        tickmode="array",
        tickvals=_year_ticks,
        ticktext=_year_ticks
    )
    bar_fig.update_yaxes(tickformat="$,.3s", gridcolor="rgba(0, 0, 0, 0.15)",
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
    my_utils.title_with_icon(value = chart_slider.value, cutoff_value = 7, title = "Small Multiples", subtitle="(Yearly Sales by Category)")
    return


@app.cell(hide_code=True)
def _(chart_slider, my_utils, segment_year_sales_df):
    from plotly.subplots import make_subplots

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
                    text=_year_value["Sales"] if chart_slider.value <= 5 else None,
                    texttemplate="%{text:$,.3s}" if chart_slider.value <= 5 else "",
                    textposition="outside",
                    cliponaxis=False,
                    showlegend=_col_idx == 1 and year == years[0],
                    hovertemplate=(f"Category={_category}<br>"
                    "Year=%{x}<br>"
                    "Sales=%{y:$,.3s}"
                    "<extra></extra>"
                    )
                ),
                row=1,
                col=_col_idx,
            )

    category_sales_subplots_fig.update_yaxes(tickformat="$,.3s", title="", gridcolor="rgba(0, 0, 0, 0.15)",gridwidth=1.05)
    category_sales_subplots_fig.update_xaxes(title="")
    category_sales_subplots_fig.update_layout(barmode="group",
                                              showlegend=False,
                                              margin = dict(t=30),
                                              height=400)
    category_sales_subplots_fig.update_annotations(font_size=14)
    mo.ui.plotly(category_sales_subplots_fig, config={"displayModeBar": False})
    return make_subplots, segment_year_sales_df_with_year_cat


@app.cell
def _():
    mo.Html("<hr>")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Horizontal Bar Charts

    Useful for unordered information. Ordered looks better in vertical.
    """)
    return


@app.cell
def _(my_utils):
    horizontal_bar_slider = mo.ui.slider(
        start=2,
        stop=12,
        value=7,
        label="Number of categories",
        show_value = True,
        full_width=True
    )

    mo.center(horizontal_bar_slider)

    _message = my_utils.callout_neutral("TODO")

    mo.hstack([_message,horizontal_bar_slider],gap=2,align="center",widths=[2,.75])
    return (horizontal_bar_slider,)


@app.cell
def _():
    horizontal_switch = mo.ui.switch(value=False, label=f"Toggle grouping by category.")
    horizontal_switch2 = mo.ui.switch(value=False, label=f"Toggle single color.")
    return horizontal_switch, horizontal_switch2


@app.cell
def _(horizontal_switch, horizontal_switch2):
    mo.hstack([horizontal_switch,horizontal_switch2])
    return


@app.cell
def _(
    base_df,
    horizontal_bar_slider,
    horizontal_switch,
    horizontal_switch2,
    make_subplots,
    my_utils,
):
    category_sales_df = (
        base_df.groupby(["Category","Sub-Category"], as_index=False)["Sales"]
        .sum()
        .rename(columns={"Sub-Category": "SubCategory"})
        .sort_values("Sales", ascending=False)
        .head(horizontal_bar_slider.value)
        .sort_values("Sales", ascending=False)
    )

    # get the count of unique categories

    _category_totals_for_legend = (
        category_sales_df.groupby("Category", as_index=False)["Sales"]
        .sum()
        .set_index("Category")["Sales"]
        .to_dict()
    )

    _category_legend_labels = {
        _cat: f"{_cat} (${numerize.numerize(_total)})"
        for _cat, _total in _category_totals_for_legend.items()
    }

    _category_sales_fig = px.bar(
        category_sales_df,
        x="Sales",
        y="SubCategory",
        orientation="h",
        text="Sales",
        color="Category" if horizontal_switch2.value else None,
        title=None,
        color_discrete_sequence=my_utils.COLOR_PALETTE
    )

    for _trace in _category_sales_fig.data:
        _original_category = _trace.name
        _trace.hovertemplate = (
            f"Category={_original_category}<br>"
            "SubCategory=%{y}<br>"
            "Sales=%{x:$,.3s}"
            "<extra></extra>"
        )
        _trace.name = _category_legend_labels.get(_original_category, _original_category)

    _category_sales_fig.update_traces(
        texttemplate="%{text:$,.3s}",
        textposition="outside",
    )

    _category_sales_fig.update_xaxes(title=None, tickformat="$,.0s")
    _category_sales_fig.update_yaxes(title=None, ticksuffix="   ")
    _category_sales_fig.update_layout(
        showlegend=True,
        height=max(320, int(horizontal_bar_slider.value * 36 + (category_sales_df["Category"].nunique() * 40))),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            title = "",
            xanchor="left",
            x=0,
            font=dict(size=14),
        ),
        margin=dict(l=10, r=10, t=50, b=10),
        yaxis={'categoryorder':'total ascending'}
    )

    _small_multiples_source_df = (
        base_df.groupby(["Category", "Sub-Category"], as_index=False)["Sales"]
        .sum()
        .rename(columns={"Sub-Category": "SubCategory"})
        .sort_values("Sales", ascending=False)
        .head(horizontal_bar_slider.value)
        .sort_values("Sales", ascending=False)
    )

    _top_categories_for_small_multiples = (
        _small_multiples_source_df.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(min(4, _small_multiples_source_df["Category"].nunique()))["Category"]
        .tolist()
    )

    _small_multiples_filtered_df = _small_multiples_source_df[
        _small_multiples_source_df["Category"].isin(_top_categories_for_small_multiples)
    ].copy()

    _small_multiples_color_map = {
        _cat: my_utils.COLOR_PALETTE[i % len(my_utils.COLOR_PALETTE)]
        for i, _cat in enumerate(_top_categories_for_small_multiples)
    }

    _small_multiples_bar_counts = (
        _small_multiples_filtered_df.groupby("Category")["SubCategory"]
        .nunique()
        .reindex(_top_categories_for_small_multiples)
        .fillna(0)
        .astype(int)
    )

    _small_multiples_row_heights = _small_multiples_bar_counts.tolist()

    _small_multiples_category_totals = (
        _small_multiples_filtered_df.groupby("Category")["Sales"]
        .sum()
        .reindex(_top_categories_for_small_multiples)
    )

    _small_multiples_subplot_titles = [
        f"{_cat} (${numerize.numerize(_small_multiples_category_totals[_cat])})"
        for _cat in _top_categories_for_small_multiples
    ]

    _small_multiples_fig = make_subplots(
        rows=len(_top_categories_for_small_multiples),
        cols=1,
        shared_xaxes=True,
        subplot_titles=_small_multiples_subplot_titles,
        vertical_spacing=0.08,
        row_heights=_small_multiples_row_heights,
    )

    for _row_idx, _cat in enumerate(_top_categories_for_small_multiples, start=1):
        _cat_df = (
            _small_multiples_filtered_df[_small_multiples_filtered_df["Category"] == _cat]
            .sort_values("Sales", ascending=True)
        )

        _small_multiples_fig.add_trace(
            go.Bar(
                x=_cat_df["Sales"],
                y=_cat_df["SubCategory"],
                orientation="h",
                marker_color=_small_multiples_color_map[_cat],
                text=_cat_df["Sales"],
                texttemplate="%{text:$,.2s}",
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    f"Category={_cat}<br>"
                    "Sub-Category=%{y}<br>"
                    "Sales=%{x:$,.2s}"
                    "<extra></extra>"
                ),
                showlegend=False,
            ),
            row=_row_idx,
            col=1,
        )

    _small_multiples_fig.update_xaxes(
        tickformat="$,.0s", title=None, showgrid=True, gridcolor="rgba(0,0,0,0.1)"
    )
    _small_multiples_fig.update_yaxes(title=None, ticksuffix="   ")
    _small_multiples_fig.update_layout(
        height=max(320, int(_small_multiples_bar_counts.sum() * 36 + len(_top_categories_for_small_multiples) * 40)),
        margin=dict(t=40, l=20, r=20, b=20),
    )

    mo.ui.plotly(_small_multiples_fig if horizontal_switch.value else _category_sales_fig, config={"displayModeBar": False})
    return


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
    ### 📈 **Overlapping** (Yearly Sales by Category)
    """)
    return


@app.cell
def _():
    fig_switch = mo.ui.switch(value=False, label=f"Highlighting a single category within many overlapping lines can focus the story.")
    return (fig_switch,)


@app.cell
def _(fig_switch, line_chart_slider):
    _pointer = mo.md((line_chart_slider.value - 3) * "👈👈")
    mo.hstack([fig_switch,_pointer],align="start",justify="start",gap=0)
    return


@app.cell
def lines_overlapping(
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
    line_categories = line_top_categories.tolist()
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
    line_all_categories_fig.update_traces(marker=dict(size=8))
    line_all_categories_fig.update_yaxes(tickformat="$,.0s",rangemode="tozero")
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




    first_category = line_categories[-1]

    line_highlight_fig = px.line(
        line_filtered_category_sales_df,
        x="Year",
        y="Sales",
        color="Category",
        markers=True,
        title=(
            f"One of the biggest categories, "
            f"<span style='color: {line_category_colors[first_category]}; text-decoration: underline;'>"
            f"{first_category}</span>, needs more attention."
        ),
        subtitle="Category sales by year"
    )

    for trace in line_highlight_fig.data:
        is_focus = trace.name == first_category
        trace.update(
            line=dict(
                color=line_category_colors[first_category] if is_focus else "rgba(180, 180, 180, 0.75)",
                width=4 if is_focus else 2
            ),
            marker=dict(
                color=line_category_colors[first_category] if is_focus else "rgba(180, 180, 180, 0.75)",
                size=9 if is_focus else 5
            ),
            opacity=1.0 if is_focus else 0.5
        )

    line_highlight_fig.update_yaxes(tickformat="$,.0s", rangemode="tozero")
    line_highlight_fig.update_xaxes(title="")
    line_highlight_fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        margin=dict(t=50),
        title=dict(font=dict(size=20, weight="bold")),
        # legend=dict(
        #     orientation="h",
        #     yanchor="bottom",
        #     y=1.02,
        #     title = "",
        #     xanchor="left",
        #     x=0,
        #     font=dict(size=14),
        # ),
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
    ### 📈 **Small Multiples** (Category Sales by Year)
    """)
    return


@app.cell(hide_code=True)
def lines_small_multiples(
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
                marker=dict(color=line_category_colors[_category],size=8),
                showlegend=False,
                hovertemplate=(f"Category={_category}<br>"
                    "Year=%{x}<br>"
                    "Sales=%{y:$,.3s}"
                    "<extra></extra>"
                )
            ),
            row=1,
            col=_col_idx,
        )

    line_category_sales_subplots_fig.update_yaxes(tickformat="$,.3s", title="", rangemode="tozero")
    line_category_sales_subplots_fig.update_xaxes(title="")
    line_category_sales_subplots_fig.update_layout(barmode="group",
                                              showlegend=False,
                                              margin = dict(t=30),
                                              height=400)
    line_category_sales_subplots_fig.update_annotations(font_size=14)
    mo.ui.plotly(line_category_sales_subplots_fig,config={"displayModeBar": False})
    return


@app.cell
def _():
    mo.Html("<hr>")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Pie Charts

    TODO: direct labeling and hard to process arcs
    """)
    return


@app.cell
async def _(my_utils):
    _img = await my_utils.gh_pages_load_image("pie.jpg")
    mo.hstack([_img,mo.md("**Pie Chart:** This chart type is great for showing how a total is divided into parts, especially when you want to emphasize the proportion of each category to the whole. However, they can become **difficult to interpret with too many categories** or **similar values**. Consider using a pie chart when you have a small number of categories (ideally 3 or fewer) and when the goal is to show the relative contribution of each category to the total. For larger numbers of categories, consider alternative visualizations like a stacked bar chart.")],gap=2,align="center",widths=[.25,1])
    return


@app.cell
def _():
    category_slider = mo.ui.slider(start=1, stop=8, value=1, label = "Number of highlighted categories", show_value = True,full_width=True)
    return (category_slider,)


@app.cell
def _(category_slider, my_utils):
    _message_by_range = [
        {"min": 1, "max": 3, "message": my_utils.callout_info("TODO")},
        {"min": 4, "max": float("inf"), "message": my_utils.callout_danger("TODO")},
    ]

    _message = next(
        item["message"]
        for item in _message_by_range
        if item["min"] <= category_slider.value <= item["max"]
    ) 

    mo.hstack([_message,category_slider],gap=2,align="center",widths=[2,.75])
    return


@app.cell(hide_code=True)
def pie_prep(base_df, category_slider):
    segment_sales_base_df = (
        base_df.groupby(["Sub-Category"], as_index=False)["Sales"]
        .sum()
        # filter all categories out with under 700k of sales
        .query("Sales >= 400000")
        .rename(columns={"Sub-Category": "Category"})
        .sort_values("Sales", ascending=False)
    )

    _top_categories_df = segment_sales_base_df.head(category_slider.value).copy()
    _other_sales = segment_sales_base_df.iloc[category_slider.value:]["Sales"].sum()

    segment_sales_df = (
        pd.concat(
            [
                _top_categories_df,
                pd.DataFrame([{"Category": "Other", "Sales": _other_sales}])
                if _other_sales > 0
                else pd.DataFrame(columns=["Category", "Sales"]),
            ],
            ignore_index=True,
        )
        #.sort_values("Sales", ascending=True)
        .reset_index(drop=True)
    )
    return segment_sales_base_df, segment_sales_df


@app.cell
def _(category_slider, my_utils, segment_sales_df):
    _total_sales = segment_sales_df["Sales"].sum()
    my_utils.title_with_icon(value = category_slider.value, cutoff_value = 3, no_icon="⚠️",no_color=my_utils.COLOR_PALETTE[7], title = "Pie Chart", subtitle=f"(Category Sales Split, Total: ${_total_sales / 1_000_000:,.2f}M)")
    return


@app.cell(hide_code=True)
def pie(my_utils, segment_sales_base_df, segment_sales_df):
    _pie_color_map = {
        category: my_utils.COLOR_PALETTE[i % len(my_utils.COLOR_PALETTE)]
        for i, category in enumerate(segment_sales_df["Category"])
        if category != "Other"
    }
    _pie_color_map["Other"] = "#D9DCFA"

    _pie_fig = px.pie(
        segment_sales_df.reset_index(drop=True),
        names="Category",
        values="Sales",
        title="",
        color="Category",
        color_discrete_map=_pie_color_map,
        height=450,
    )
    _pie_fig.update_traces(
        textposition="inside",
        texttemplate="%{label}<br>%{percent} (%{value:$.3s})",
        sort=False,
        direction="clockwise",
        hoverinfo="skip",
        hovertemplate=None
    )
    _pie_fig.update_layout(showlegend = False)


    # START SEGMENT FOR STACKED BAR CHART OF OTHER CATEGORIES
    selected_categories_for_pie = set(
        segment_sales_df.loc[segment_sales_df["Category"] != "Other", "Category"].tolist()
    )

    other_categories_detail_df = (
        segment_sales_base_df.loc[
            ~segment_sales_base_df["Category"].isin(selected_categories_for_pie)
        ]
        .sort_values("Sales", ascending=False)
        .reset_index(drop=True)
    )

    other_categories_stack_df = other_categories_detail_df.assign(Group="Other Categories")
    _all_total_sales = segment_sales_base_df["Sales"].sum()
    other_categories_stack_df["_percent"] = (
        other_categories_stack_df["Sales"] / _all_total_sales
    )
    other_categories_stack_df["_percent_label"] = (
        other_categories_stack_df["_percent"].map(lambda x: f"{x:.1%}"))
    other_categories_stack_df["_segment_label"] = (
        other_categories_stack_df["Category"]
    )

    other_stacked_bar_fig = px.bar(
        other_categories_stack_df,
        x="Group",
        y="_percent",
        color="Category",
        barmode="stack",
        color_discrete_sequence=my_utils.COLOR_PALETTE[
            len(selected_categories_for_pie) : len(selected_categories_for_pie) + len(other_categories_stack_df)
        ][::1],
        hover_data={"Sales": ":,.0f", "Group": False, "_percent_label": True},
        text="_segment_label"
    )

    other_stacked_bar_fig.update_traces(
        texttemplate="%{text}<br>%{value:.1%} (%{customdata[0]:$.2s})",
        textposition="inside",
        hoverinfo="skip",
        hovertemplate=None
    )

    other_stacked_bar_fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        legend_title=None,
        showlegend=False,
        height=450,
        width=350
    )

    other_stacked_bar_fig.update_yaxes(tickformat=".1%")


    mo.hstack([_pie_fig,other_stacked_bar_fig],gap=0,align="center",justify="center",widths=[.65,.35])
    return


@app.cell
def _():
    mo.Html("<hr>")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Donut Charts and Gauge Charts

    These two chart types are great for quick diagnostic visualization of single continuous values in relationship to the whole (or another target value). Consider the story you're trying to tell with this single value chart.
    """)
    return


@app.cell
async def _(my_utils):
    _img = await my_utils.gh_pages_load_image("donut.jpg")
    mo.hstack([_img,mo.md("**Donut Chart**: This chart type is useful for representing **single values as a percentage of the whole**. A quick glance at a single donut chart can emphasize impact. While not represented in this guide, splitting a donut chart into multiple categories should follow the same rules of pie charts: **too many categories introduces visual overwhelm**.")],gap=2,align="center",widths=[.25,1])
    return


@app.cell
async def _(my_utils):
    _img = await my_utils.gh_pages_load_image("gauge.jpg")
    mo.hstack([_img,mo.md("**Gauge Chart**: This chart type is useful for comparing a value against a target or a set of milestones. It emphasizes the coninuum of values along a desired goal or risk factors.")],gap=2,align="center",widths=[.25,1])
    return


@app.cell
def _(my_utils):
    _message = my_utils.callout_neutral("Depending on the goal of the chart, how might you represent the data of a single category?")

    donut_slider = mo.ui.slider(start=0, stop=1, step=.01, value=.50, label = "Percentage of Sales", show_value = True, debounce=True,full_width=True)
    mo.hstack([_message,donut_slider],gap=2,align="center",widths=[2,.75])
    return (donut_slider,)


@app.cell
def _(donut_slider, my_utils):
    _phone_share = min(max(float(donut_slider.value), 0.0), 1.0)
    _phone_share_dollar = "$" + numerize.numerize(_phone_share * 11000000)

    _phone_donut_fig = px.pie(
        names=["Phone", "Other"],
        values=[_phone_share, 1 - _phone_share],
        color=["Phone", "Other"],
        color_discrete_map={"Phone": my_utils.COLOR_PALETTE[0], "Other": "#d9dcfa"},
        hole=0.5,
        height=350,
        title="Share of Phones"
    )

    _phone_donut_fig.update_traces(
        #textposition="inside",
        #texttemplate="%{label}<br>%{percent}",
        #hoverinfo="none",
        textinfo="none",
        sort=False,
    )

    _phone_donut_fig.update_layout(showlegend=False,title_x=0.5,margin=dict(t=60),title_font=dict(size=22,weight="bold"))

    _label = f"{_phone_share:.0%}<br>({_phone_share_dollar})"
    _phone_donut_fig.add_annotation(
        x=0.5,
        y=0.51,
        text=_label,
        showarrow=False,
        font=dict(size=26,weight="bold"),
    )

    #Use Plotly Indicator’s `number.prefix` (and optionally `delta.prefix`) fields.

    _gauge_fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=donut_slider.value * 11000000,
            number={"valueformat": "$.3s","font": {"size": 40, "weight": "bold"}},
            delta={
                "reference": 7500000,
                "valueformat": "$.3s",
                "increasing": {"color": my_utils.COLOR_PALETTE[0]},
                "decreasing": {"color": my_utils.COLOR_PALETTE[2]},
                "font": {"size": 26, "weight": "bold"}
            },
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Phone Sales (vs. Target)", "font": {"size": 20, "weight": "bold"}},
            gauge={
                "axis": {
                    "range": [None, 11000000],
                    "tickwidth": 1,
                    "tickcolor": "darkblue",
                    "tickformat": "$.3s",
                    "tickvals": [0, 2500000, 5000000, 7500000, 10000000,11000000], # Specify the values where ticks appear

                },
                "bar": {"color": my_utils.COLOR_PALETTE[0]},
                "bordercolor": "gray",
                "steps": [
                    {"range": [0, 7500000], "color": "#d9dcfa"}
                ],
                "threshold": {
                    "line": {"color": my_utils.COLOR_PALETTE[1], "width": 8},
                    "thickness": 1,
                    "value": 7500000
                },
            },
        )
    )

    # add margin
    _gauge_fig.update_layout(height=325)

    mo.hstack([mo.ui.plotly(_phone_donut_fig, config={"displayModeBar": False}),mo.ui.plotly(_gauge_fig, config={"displayModeBar": False})],gap=0,widths=[.45,.55],align="center",justify="center")
    return


@app.cell
def _():
    mo.Html("<hr>")
    return


if __name__ == "__main__":
    app.run()
