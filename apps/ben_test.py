import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")

with app.setup:
    import plotly.express as px
    import pandas as pd
    import matplotlib.pyplot as plt
    import marimo as mo
    import plotly.io as pio

    # set plotly default template and disable mode bar
    pio.templates.default = "plotly_white"
    #pio.templates["plotly_white"].layout.margin = dict(t=0, b=0)
    for renderer_name in pio.renderers.default.split('+'):
        pio.renderers[renderer_name].config['displayModeBar'] = False


@app.cell(hide_code=True)
def _():
    #prep data
    path_to_csv = mo.notebook_location() / "public" / "superstore.csv"
    base_df = pd.read_csv(path_to_csv)

    base_df_with_year = base_df.assign(
        _order_year=pd.to_datetime(base_df["Order Date"]).dt.year
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
    Consider a vertical bar chart of many categories. Depending on what story you're looking to tell, there are usually two ways to group the bars.

    **Grouped or Clustered Bar Chart**: In this format, bars representing different categories are placed side by side for each group (e.g., year). This allows for easy comparison of categories within the same group while still getting a sense for overall trend. However, if there are too many categories, it can become visually overwhelming and difficult to interpret.

    **Small Multiples**: In this format, each category gets its own individual chart (or subplot) that shares the same axes. This allows for easier comparison of trends across categories without the visual clutter of a grouped bar chart. However, it can be more difficult to compare values across categories since they are not visually grouped together. Tip: consider adding darker axis lines to allow easier comparison across groups.

    The slider below modifies the number of categories shown in the charts. Experiment with which chart type might be the most effective for the number of categories shown as they related to the goal of the visual (showing **intra-year comparisons** vs. **individual trends**).
    """)
    return


@app.cell
def _():
    mo.callout("Consider keeping the number of categories to a maximum of 7 or 8 to reduce visual overwhelm. If you need more try consolidating categories or providing a table view instead.", "warn")
    return


@app.cell(hide_code=True)
def _():
    segment_slider = mo.ui.slider(
        start=1,
        stop=10,
        value=5,
        label="Number of categories",
    )
    segment_slider
    return (segment_slider,)


@app.cell(hide_code=True)
def _(segment_slider, segment_year_sales_df):
    top_subcats = (
        segment_year_sales_df.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(segment_slider.value)["Category"]
    )

    filtered_segment_year_sales_df = segment_year_sales_df[
        segment_year_sales_df["Category"].isin(top_subcats)
    ]

    bar_fig = px.bar(
        filtered_segment_year_sales_df,
        x="Year",
        y="Sales",
        color="Category",
        barmode="group"
    )

    _year_ticks = sorted(filtered_segment_year_sales_df["Year"].unique())
    bar_fig.update_xaxes(tickmode="array", tickvals=_year_ticks, ticktext=_year_ticks)
    bar_fig.update_yaxes(tickformat="$,.0f")
    bar_fig.update_layout(xaxis_title=None, yaxis_title=None,legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    bar_fig
    return


@app.cell(hide_code=True)
def _(segment_slider, segment_year_sales_df):
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    segment_year_sales_df_with_year_cat = segment_year_sales_df.assign(
        Year=segment_year_sales_df["Year"].astype(str)
    )

    top_categories = (
        segment_year_sales_df_with_year_cat.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(segment_slider.value)["Category"]
    )

    filtered_category_sales_df = segment_year_sales_df_with_year_cat[
        segment_year_sales_df_with_year_cat["Category"].isin(top_categories)
    ]

    years = sorted(filtered_category_sales_df["Year"].unique())
    categories = sorted(top_categories.tolist())
    color_sequence = px.colors.qualitative.Plotly
    category_colors = {
        category: color_sequence[i % len(color_sequence)]
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

    category_sales_subplots_fig.update_yaxes(tickformat="$,.0f", title="")
    category_sales_subplots_fig.update_xaxes(title="")
    category_sales_subplots_fig.update_layout(barmode="group", showlegend=False)
    category_sales_subplots_fig.update_annotations(font_size=14)
    category_sales_subplots_fig
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
    Similarly, consider a line chart of the same information. How does the choice between a single line chart with all categories vs. small multiples of line charts affect your ability to compare trends across categories and within categories? Does the number of categories shown change which chart type is more effective for the story you're trying to tell?
    """)
    return


@app.cell(hide_code=True)
def _(filtered_category_sales_df):
    line_all_categories_fig = px.line(
        filtered_category_sales_df,
        x="Year",
        y="Sales",
        color="Category",
        markers=True,
        title=""
    )
    line_all_categories_fig.update_yaxes(tickformat="$,.0f",rangemode="tozero")
    line_all_categories_fig.update_xaxes(title="")
    line_all_categories_fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    line_all_categories_fig
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
    line_category_sales_subplots_fig.update_layout(showlegend=False)
    line_category_sales_subplots_fig.update_annotations(font_size=14)
    line_category_sales_subplots_fig
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
 
    """)
    return


if __name__ == "__main__":
    app.run()
