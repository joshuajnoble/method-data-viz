# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "plotly",
#     "marimo",
#     "pandas",
# ]
# ///

import marimo as mo

__generated_with = "0.19.7"
app = mo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import plotly.graph_objects as go
    import pandas as pd

    @mo.cache
    def get_yearly_by_segment():

        #path_to_csv = mo.notebook_location() / "public" / "yearly_sales_by_segment.csv"
        path_to_csv = "https://raw.githubusercontent.com/joshuajnoble/method-data-viz/refs/heads/main/apps/public/yearly_sales_by_segment.csv"
        yearly_by_segment = pd.read_csv(path_to_csv)
        return yearly_by_segment
    
    return (mo,)

@app.cell
def _():
    mo.md(
        """
        
        # Percentages and Segments

        When you want to see what makes up a whole, for instance, all customers in Australia or all sales in 2011, it's helpful to figure out how much of the whole each segment represents. 
        The classic way to represent this is with a pie chart.
        """)
    
@app.cell()
def _(mo):
    mo.image(src="https://github.com/joshuajnoble/method-data-viz/blob/main/apps/public/piechart.png")

@app.cell()
def _(mo):
    mo.md(
        """

        Pie charts show how much of a whole different segments make. This is a row-wise (per observation) percentage where we have multiple segments within a single observation (like a single year) and we want to see what fraction each segment contributes to that row.

        The limitation of a pie chart is that it only allows you to show one 'whole' at a time. When you want to show more than 1 'whole' and compare them, you might look at a stacked bar chart or an area chart.
        
        The limitation of a stacked bar chart is that it's difficult to compare how much a segment contributes to different wholes. 
        If you want to know how much of sales went to Asia in 2011 versus 2012, you're wanting to know what percentage of all sales Asia contributed in 2011 vs 2012. That's different than knowing the total amount of sales that went to Asia in 2011 and 2012.

        Again, knowing what story you're trying to tell will inform which chart is the most appropriate. Take a look at the same data visualized with 4 different types of charts.
        
        """
    )
    return

@app.cell()
def _(mo):

        
    df = get_yearly_by_segment().pivot(index="year", columns="Segment", values="sales")
    df = df.reset_index()
    df.columns = df.columns.astype(str)

    segments = ["Consumer","Corporate","Home Office"]

    normed_segments = ["Consumer_norm","Corporate_norm","Home Office_norm"]
    df[normed_segments] = df[segments].div(df[segments].sum(axis=1), axis=0)

    fig = go.Figure()

    tick_vals = [2011, 2012, 2013, 2014]

    # --- PIE TRACE (default year) ---
    year_idx = 0
    fig.add_trace(
        go.Pie(
            labels=segments,
            values=df.loc[year_idx, segments],
            name="Pie",
            visible=True
        )
    )

    # --- STACKED BAR TRACES ---
    for seg in segments:
        fig.add_trace(
            go.Bar(
                x=df["year"],
                y=df[seg],
                name=seg,
                visible=False
            )
        )

    # --- STACKED NORM BAR TRACES ---
    for seg in normed_segments:
        fig.add_trace(
            go.Bar(
                x=df["year"],
                y=df[seg],
                name=seg,
                visible=False
            )
        )

    # --- AREA TRACES ---
    for seg in segments:
        fig.add_trace(
            go.Scatter(
                x=df["year"],
                y=df[seg],
                stackgroup="one",
                mode="lines",
                name=seg,
                visible=False
            )
        )

    fig.update_layout({"title":{"text":"2011 Sales By Category", 'x': 0.4}, "xaxis": {"visible": False}, "yaxis": {"visible": False},})

    fig.update_layout(
        updatemenus=[
            dict(
                type="dropdown",
                direction="down",
                buttons=[
                    dict(
                        label="Pie",
                        method="update",
                        args=[
                            {"visible":[True, False, False, False, False, False, False, False, False, False]},
                            {
                                "xaxis":{"visible":False},
                                "yaxis":{"visible":False},
                                "title":{"text":"2011 Sales By Category", 'x': 0.4}
                            }
                        ]
                    ),
                    dict(
                        label="Stacked Bar",
                        method="update",
                        args=[
                            {"visible":[False, True, True, True, False, False, False, False, False, False]},
                            {
                                "xaxis":{"visible":True},
                                "yaxis":{"visible":True},
                                "barmode":"stack",
                                "title":{"text":"Yearly Sales By Category In USD", 'x': 0.4}
                            }
                        ]
                    ),
                    dict(
                        label="Normalized Stacked Bar",
                        method="update",
                        args=[
                            {"visible":[False, False, False, False, True, True, True, False, False, False]},
                            {
                                "xaxis":{"visible":True},
                                "yaxis":{"visible":True},
                                "barmode":"stack",
                                "title":{"text":"Composition of Sales By Category", 'x': 0.4}
                            }
                        ]
                    ),
                    dict(
                        label="Area",
                        method="update",
                        args=[
                            {"visible":[False, False, False, False, False, False, False, True, True, True]},
                            {
                                "xaxis":{"visible":True, "tickmode":"array", "tickvals":tick_vals},
                                "yaxis":{"visible":True},
                                "title":{"text":"Yearly Sales By Category In USD", 'x': 0.4}
                            }
                        ]
                    )
                ]
            )
        ]
    )

    mo.ui.plotly(fig, config={"displayModeBar": False})



if __name__ == "__main__":
    app.run()