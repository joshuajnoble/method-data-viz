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


@app.cell
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
    segment_slider = mo.ui.slider(
        start=1,
        stop=10,
        value=5,
        label="Number of segments",
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


@app.cell
def _(segment_slider, segment_year_sales_df):
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    _segment_year_sales_df_with_year_cat = segment_year_sales_df.assign(
        Year=segment_year_sales_df["Year"].astype(str)
    )

    _top_categories = (
        _segment_year_sales_df_with_year_cat.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(segment_slider.value)["Category"]
    )

    _filtered_category_sales_df = _segment_year_sales_df_with_year_cat[
        _segment_year_sales_df_with_year_cat["Category"].isin(_top_categories)
    ]

    _years = sorted(_filtered_category_sales_df["Year"].unique())
    _categories = sorted(_top_categories.tolist())
    _color_sequence = px.colors.qualitative.Plotly
    _category_colors = {
        category: _color_sequence[i % len(_color_sequence)]
        for i, category in enumerate(_categories)
    }

    _category_sales_subplots_fig = make_subplots(
        rows=1,
        cols=len(_categories),
        shared_yaxes=True,
        subplot_titles=_categories,
    )

    for col_idx, category in enumerate(_categories, start=1):
        _category_df = _filtered_category_sales_df[
            _filtered_category_sales_df["Category"] == category
        ].sort_values("Year")
        for year in _years:
            _year_value = _category_df[_category_df["Year"] == year]
            _category_sales_subplots_fig.add_trace(
                go.Bar(
                    x=_year_value["Year"],
                    y=_year_value["Sales"],
                    name=category,
                    marker_color=_category_colors[category],
                    showlegend=col_idx == 1 and year == _years[0],
                ),
                row=1,
                col=col_idx,
            )

    _category_sales_subplots_fig.update_yaxes(tickformat="$,.0f", title="")
    _category_sales_subplots_fig.update_xaxes(title="")
    _category_sales_subplots_fig.update_layout(barmode="group", showlegend=False)
    _category_sales_subplots_fig.update_annotations(font_size=14)
    _category_sales_subplots_fig
    return


if __name__ == "__main__":
    app.run()
