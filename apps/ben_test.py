import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import plotly.express as px
    import pandas as pd
    import matplotlib.pyplot as plt
    import marimo as mo

    return mo, pd, px


@app.cell
def _(mo, pd):
    # Load the data
    path_to_csv = mo.notebook_location() / "public" / "superstore.csv"
    base_df = pd.read_csv(path_to_csv)
    return (base_df,)


@app.cell
def _(base_df, pd):
    base_df_with_year = base_df.assign(
        _order_year=pd.to_datetime(base_df["Order Date"]).dt.year
    )
    segment_year_sales_df = (
        base_df_with_year.groupby(["_order_year", "Sub-Category"], as_index=False)["Sales"]
        .sum()
        .rename(columns={"_order_year": "Year","Sub-Category":"Category"})
    )
    segment_year_sales_df
    return (segment_year_sales_df,)


@app.cell(hide_code=True)
def _(mo):
    segment_slider = mo.ui.slider(
        start=1,
        stop=10,
        value=5,
        label="Number of segments",
    )
    segment_slider
    return (segment_slider,)


@app.cell(hide_code=True)
def _(px, segment_slider, segment_year_sales_df):
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
        barmode="group",
        labels={"Sales": "", "Year": ""},
    )

    _year_ticks = sorted(filtered_segment_year_sales_df["Year"].unique())
    bar_fig.update_xaxes(tickmode="array", tickvals=_year_ticks, ticktext=_year_ticks)
    bar_fig.update_yaxes(tickformat="$,.0f")
    bar_fig.update_layout(xaxis_title=None, yaxis_title=None)

    bar_fig
    return


if __name__ == "__main__":
    app.run()
