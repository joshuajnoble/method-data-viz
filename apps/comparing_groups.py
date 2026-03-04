# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.20.2",
#     "plotly",
#     "pandas",
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
    import utils

    # set plotly default template and disable mode bar
    utils.run_plotly_defaults()


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Comparing Multiple Groups

    The focus of this section is to address the most effective ways to compare multiple groups and the specific story you're trying to tell with the data.
    """)
    return


@app.cell(hide_code=True)
async def _():
    # prep data
    base_df = await utils.gh_pages_read_csv_into_df("superstore.csv")

    base_df_with_year = base_df.assign(
        _order_year=pd.to_datetime(base_df["Order Date"], format="%m/%d/%y").dt.year
    )
    segment_year_sales_df = (
        base_df_with_year.groupby(["_order_year", "Sub-Category"], as_index=False)["Sales"]
        .sum()
        .rename(columns={"_order_year": "Year","Sub-Category":"Category"})
    )
    return (segment_year_sales_df,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Vertical Bar Charts

    Consider a vertical bar chart of many categories. Depending on what story you're looking to tell, there are usually two ways to group the bars.

    **Grouped or Clustered Bar Chart**: In this format, bars representing different categories are placed side by side for each group (e.g., year). This allows for easy *comparison of categories within the same group/cluster* while still getting a sense for the overall trend. However, if there are too many categories, it can become *visually overwhelming* and difficult to interpret.

    **Small Multiples**: In this format, each category gets its own individual chart (or subplot) that shares the same axes. This allows for *easier comparison of trends across categories* without the visual clutter of a grouped bar chart. However, it can be more difficult to compare values across categories since they are not visually grouped together. Tip: consider adding darker axis lines to allow easier comparison across groups.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    > <u>The slider below</u> 👇 changes the number of categories shown in the charts following. Experiment with which chart type might be the most effective for the **number of categories** as they relate to the **goal of the visual representation**. How might you focus the experience on showing **intra-year comparisons** vs. **individual trends**?
    """)
    return


@app.cell(hide_code=True)
def _():
    chart_slider = mo.ui.slider(
        start=1,
        stop=10,
        value=3,
        label="Number of categories",
        show_value = True,
    )

    mo.center(chart_slider)
    return (chart_slider,)


@app.cell(hide_code=True)
def callout_barchart(chart_slider):
    # callout
    _message_by_range = [
        {"min": 1, "max": 3, "message": utils.callout_info("<b>1-3</b>: This number of categories is typically manageable in a <b>grouped bar chart</b>. It focuses on <b>intra-year comparisons</b> while still allowing for some comparison across years. <b>Small multiples</b> will also work well for this number of categories and can help to emphasize <b>individual trends</b>.")},
        {"min": 4, "max": 7, "message": utils.callout_info("<b>4-7</b>: This number of categories is great for a <b>small multiples chart</b> and showing <b>individual trends</b> while still allowing for comparison across categories. It's on the higher end for a <b>grouped bar chart</b> and can introduce visual overwhelm.")},
        {"min": 8, "max": float("inf"), "message": utils.callout_danger("<b>8+</b>: This number of categories will introduce <b>visual overwhelm with either chart type</b>. If you need more than 7 categories, try <b>consolidating categories or providing a table view instead.</b>")},
    ]

    _message = next(
        item["message"]
        for item in _message_by_range
        if item["min"] <= chart_slider.value <= item["max"]
    )

    _message
    return


@app.cell(hide_code=True)
def _(chart_slider):
    _heading_color = utils.COLOR_PALETTE[0] if 1 <= chart_slider.value <= 3 else  utils.COLOR_PALETTE[2]
    mo.md(
        f"""
    ### <span style="color: {_heading_color};">**Grouped Bar Chart** (Category Sales by Year)</span>
    """
    )
    return


@app.cell(hide_code=True)
def _(chart_slider, segment_year_sales_df):
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
        color_discrete_sequence=utils.COLOR_PALETTE[:len(top_subcats)]
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


@app.cell(hide_code=True)
def _(chart_slider):
    _heading_color = utils.COLOR_PALETTE[0] if 1 <= chart_slider.value <= 7 else  utils.COLOR_PALETTE[2]
    mo.md(
        f"""
    ### <span style="color: {_heading_color};">**Small Multiples** (Yearly Sales by Category)</span>
    """
    )
    return


@app.cell(hide_code=True)
def _(chart_slider, segment_year_sales_df):
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
        category: utils.COLOR_PALETTE[i % len(utils.COLOR_PALETTE)]
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
    return (
        categories,
        category_colors,
        filtered_category_sales_df,
        go,
        make_subplots,
    )


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Line Charts
    Similarly, consider a line chart of the same information. How does the choice between a single line chart with all categories vs. small multiples of line charts affect your ability to compare trends across categories and within categories? Does the number of categories shown change which chart type is more effective for the story you're trying to tell?
    """)
    return


@app.cell
def _(chart_slider):
    mo.center(chart_slider)
    return


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
def _(categories, category_colors, fig_switch, filtered_category_sales_df):
    line_all_categories_fig = px.line(
        filtered_category_sales_df,
        x="Year",
        y="Sales",
        color="Category",
        markers=True,
        title="",
        color_discrete_sequence=utils.COLOR_PALETTE[:len(categories)]
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




    first_category = categories[0] if len(categories) > 0 else None

    line_highlight_fig = px.line(
        filtered_category_sales_df,
        x="Year",
        y="Sales",
        color="Category",
        markers=True,
    )

    for trace in line_highlight_fig.data:
        if trace.name == first_category:
            trace.update(line=dict(color=category_colors[first_category], width=3), marker=dict(color=category_colors[first_category], size=9))
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
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### **Small Multiples** (Category Sales by Year)
    """)
    return


@app.cell(hide_code=True)
def _(
    categories,
    category_colors,
    filtered_category_sales_df,
    go,
    make_subplots,
):
    line_category_sales_subplots_fig = make_subplots(
        rows=1,
        cols=len(categories),
        shared_yaxes=True,
        subplot_titles=categories,
    )

    for _col_idx, _category in enumerate(categories, start=1):
        _category_df = filtered_category_sales_df[
            filtered_category_sales_df["Category"] == _category
        ].sort_values("Year")
        line_category_sales_subplots_fig.add_trace(
            go.Scatter(
                x=_category_df["Year"],
                y=_category_df["Sales"],
                mode="lines+markers",
                name=_category,
                line=dict(color=category_colors[_category]),
                marker=dict(color=category_colors[_category]),
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
 
    """)
    return


if __name__ == "__main__":
    app.run()
